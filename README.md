# Google review scraper


This is my simple python script for downloading reviews from google map objects. It gathers the data into a python dict, then saves it into an excel file, containing the following features:

- **object_name**
- **object_address**	
- **overall_rating**	
- **cnt_reviews:** number of reviews	
- **object_url**
- **name:** name of the person who wrote the review	
- **date:** when was it written
- **rate**	
- **review:** the text of the review
- **reply:** the reply from the owner 

#


<table border=1 cellpadding=10><tr><td>

####  NOTICE !

---

**It only works with Google Map URLs with hungarian language!**

**I find the elements by classes and XPATHs. If Google changes its structure or renames the classes, it may be necessary to reparameterize the XPATH and class references!**

</td></tr></table>

It has been tested on 2023.02.12, and everything works fine. 


### Requirements:
- async-generator==1.10
- attrs==22.2.0
- beautifulsoup4==4.11.2
- bs4==0.0.1
- certifi==2022.12.7
- et-xmlfile==1.1.0
- exceptiongroup==1.1.0
- h11==0.14.0
- idna==3.4
- numpy==1.24.2
- openpyxl==3.1.0
- outcome==1.2.0
- pandas==1.5.3
- PySocks==1.7.1
- python-dateutil==2.8.2
- pytz==2022.7.1
- selenium==4.8.0
- six==1.16.0
- sniffio==1.3.0
- sortedcontainers==2.4.0
- soupsieve==2.3.2.post1
- trio==0.22.0
- trio-websocket==0.9.2
- urllib3==1.26.14
- wsproto==1.2.0
