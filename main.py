import time
import random
import re
import os
import logging
import pandas as pd
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.common.exceptions import NoSuchElementException


DRIVER_PATH = r'/home/oli/Projects/Google-review-scraper/chromedriver_linux64/chromedriver'
SAVING_PATH = r'/home/oli/Projects/Google-review-scraper/data'

# declaring a list, that contains the urls wich we want to be scraped
OBJECT_URLS = [
        #'https://www.google.com/maps/place/GoGo+hami+%C3%9Ajpest-k%C3%B6zpont/@47.6741137,18.6786254,11z/data=!4m7!3m6!1s0x4741da37020258d1:0xcac69f37622f45d0!8m2!3d47.5611747!4d19.0903816!15sCghnb2dvaGFtaVoKIghnb2dvaGFtaZIBCnJlc3RhdXJhbnTgAQA!16s%2Fg%2F11bwql9cb2?hl=hu&coh=164777&entry=tt&shorturl=1',
        #'https://www.google.com/maps/place/Tesco/@47.7160014,18.7379746,16.04z/data=!4m6!3m5!1s0x476a645d4983b2df:0xf8f1eb25f3813b5b!8m2!3d47.7131753!4d18.7406381!16s%2Fg%2F1hg50d6_k?hl=hu',
        'https://www.google.com/maps/place/%C3%9Ajpesti+0-24+Gy%C3%B3gyszert%C3%A1r/@47.5644325,19.0890735,15.67z/data=!4m6!3m5!1s0x4741db39cf7c4a29:0xee59438ff2a16e76!8m2!3d47.5630657!4d19.0815841!16s%2Fg%2F11fvvjvtzh?hl=hu',
    ]

# setting up the logging object
logger = logging.getLogger('main')
logging.basicConfig(
    format='[%(asctime)s] [%(levelname)s] - %(message)s',
    datefmt='%H:%M:%S'
    )

# we can change the logging level. Use logging.DEBUG if necesarry
logger.setLevel(logging.DEBUG)


def scrape_an_object(object_url: str) -> tuple :
    """
    This method will:
    - open the input URL (of a google maps object like stores, hotels, restaurants etc...)
    - accept the cookies
    - get some basic information of the given object (name, address, overall rating, 
      and the number of reviews)
    - scroll down to the bottom of the page in order to load every reviews in the html source code
    - scrape the div that contains the reviews

    args: 
        object_url: the url of the google maps object to open
    
    returns a tuple containing:
        store_main_data: a dictionary containing the basic information of the google map object 
                      (name, address, overall rating, and the number of reviews)

        reviews_source: a bs4 object containing the html source code of the div 
                        that contains all the reviews
    
    """

    # setting the chrome driver for selenium
    driver = webdriver.Chrome(service=Service(DRIVER_PATH))

    # opening the given URL
    logger.debug("Opening the given URL")
    driver.get(object_url)
    

    # accepting the cookies
    logger.debug("Accepting the cookies")
    driver.find_element(By.CLASS_NAME,"lssxud").click()

    # waiting some random seconds
    time.sleep(random.uniform(4,6))

    # I use CSS selectors where I can, because its more robust than XPATH
    object_name = driver.find_element(
        By.CSS_SELECTOR,
        'h1.DUwDvf.fontHeadlineLarge'
    ).text
    logger.debug(f'Object_name OK : {object_name}')

    object_address = driver.find_element(
        By.CSS_SELECTOR,
        'div.Io6YTe.fontBodyMedium'
    ).text
    logger.debug(f'Object_address OK : {object_address}')


    # for some reason sometimes google full randomly loads the page
    # with a slightly different page structure. to be able to handle this,
    # I created an except branch that scrapes the right objects in that scenario
    try:

        overall_rating = driver.find_element(
            By.CSS_SELECTOR,
            'div.F7nice.mmu3tf'
        ).text.split()[0]
        logger.debug(f'Overall_rating OK : {overall_rating}')

        review_number = driver.find_element(
            By.CSS_SELECTOR,
            'div.F7nice.mmu3tf'
        ).text.replace(' ','')

        review_number = int(re.compile(r'\d+').findall(review_number)[-1])
        logger.debug(f'Review_number OK : {review_number}')

        # click to load further reviews
        driver.find_element(
            By.XPATH,
            '//*[@id="QA0Szd"]/div/div/div[1]/div[2]/div/div[1]/div/div/div[2]/div[1]/div[1]/div[2]/div/div[1]/div[2]/span[2]/span[1]/span'
        ).click()

        logger.debug('Clicked to load further reviews')
    
        time.sleep(random.uniform(0.1, 0.5))

        # find scroll layout
        scrollable_div = driver.find_element(
            By.XPATH,
            '//*[@id="QA0Szd"]/div/div/div[1]/div[2]/div/div[1]/div/div/div[2]'
        )

        logger.debug('Scroll div OK')
     
    except NoSuchElementException:

        logger.debug('Except branch')

        div_num_rating = driver.find_element(
            By.CSS_SELECTOR,
            'div.F7nice'
        ).text
        overall_rating = div_num_rating.split()[0]
        logger.debug(f'Overall_rating OK : {overall_rating}')

        review_number = int(div_num_rating.split()[1].replace('(','').replace(')',''))
        logger.debug(f'Review_number OK : {review_number}')

        # click on the review tab
        driver.find_element(
            By.XPATH,
            '//*[@id="QA0Szd"]/div/div/div[1]/div[2]/div/div[1]/div/div/div[3]/div/div/button[2]/div[2]/div[2]'
        ).click()
        logger.debug('clicked to load further reviews')

        time.sleep(random.uniform(0.1, 0.5))

        # find scroll layout
        scrollable_div = driver.find_element(
            By.XPATH,
            '//*[@id="QA0Szd"]/div/div/div[1]/div[2]/div/div[1]/div/div/div[3]'
        )
        logger.debug('Scroll div OK')

    time.sleep(random.uniform(2,4))

    # scroll as many times as necessary to load all reviews
    for _ in range(0,(round(review_number/5 - 1)+1)):
        driver.execute_script(
            'arguments[0].scrollTop = arguments[0].scrollHeight',
            scrollable_div
        )
        time.sleep(random.uniform(1, 2))

    # parse the html with a bs object
    response = BeautifulSoup(driver.page_source, 'html.parser')
    reviews_source = response.find_all('div', class_='jJc9Ad')
    logger.debug('Source code has been parsed!')

    # closing the browser
    driver.close()

    # storing the data in a dict
    store_main_data = {'object_name': object_name,
                       'object_address': object_address,
                       'overall_rating': overall_rating,
                       'review_num': review_number,
                       'object_url':object_url}

    return store_main_data, reviews_source



def extract_reviews(reviews_source: list) -> list:

    r"""
    This method processes the input html code and returns a list 
    containing the reviews.

    """

    review_list = []

    logger.debug('Starting iterate trough the reviews...')
    for review in reviews_source:

        # extract the relevant informations
        user = review.find('div', class_= 'd4r55').text.strip()
        date = review.find('span', class_= 'rsqaWe').text.strip()
        rate = len(review.find('span',class_ = 'kvMYJc'))
        review_text = review.find('span', class_= 'wiI7pd')
        review_text = '' if review_text is None else review_text.text 
        reply_source = review.find('div', class_= 'CDe7pd')
        reply = reply_source.text if reply_source else '-'


        review_list.append({'name': user,
                            'date': date,
                            'rate': rate,
                            'review_text': review_text,
                            'reply': reply})

    return review_list



def main():

    scraped_data =  []

    # loop trough the urls and calling the necessary functions to populate the empty scraped_data list
    for i, url in enumerate(OBJECT_URLS):
        try:
            time.sleep(random.uniform(3,10))
            
            store_main_data, reviews_source = scrape_an_object(url)
            scraped_data.append(store_main_data)

            review_list = extract_reviews(reviews_source)
            scraped_data[i]['reviews'] = review_list

            if scraped_data[i]['review_num'] != len(scraped_data[i]['reviews']):
                logger.warning(f'For some reason not all the reviews had been scraped for the following object: {store_main_data["object_name"]}')


        except Exception as exception:
            logger.error(f'{url} \n {exception}')
            scraped_data.append(
                    {'object_name': 'Error',
                    'object_address': 'Error',
                    'overall_rating': 'None',
                    'review_num': 'None',
                    'object_url':url,
                    'reviews':[{}]
                    }
                )

        logger.info(f' {i+1} URL has been finished from the total of {len(OBJECT_URLS)}')


    # reading the dict with pandas
    result_df = pd.json_normalize(
                scraped_data,
                record_path = ['reviews'],
                errors='ignore',
                meta=['object_name', 'object_address', 'overall_rating', 'review_num', 'object_url']
                )


    # reorder the columns
    result_df = result_df[[
                'object_name','object_address','overall_rating','review_num',
                'object_url', 'name','date','rate','review_text','reply'
                ]]

    # Saving the result into an excel file
    save_path = os.path.join(SAVING_PATH,'scrape_result.xlsx')
    result_df.to_excel(
        save_path,
        index= False
    )

    logger.info(f'Successfully exported the result file in the following folder: {os.path.join(SAVING_PATH,"scrape_result.xlsx")}')


if __name__ == '__main__':
    main()

    


