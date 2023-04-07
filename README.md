# Google review scraper


This is a simple Python script that downloads reviews from Google Maps objects. It gathers the data into a Python dictionary and then saves it into an Excel file, which contains the following features:

- **object_name**
- **object_address**	
- **overall_rating**	
- **cnt_reviews:** number of reviews	
- **object_url**
- **name:** name of the person who wrote the review	
- **date:** when the review was written
- **rate**	
- **review:** the text of the review
- **reply:** the reply from the owner 

#


<table border=1 cellpadding=10><tr><td>

####  NOTICE !

---

**It only works with Google Map URLs with Hungarian language!**

**The script finds elements using classes and XPATHs. If Google changes its structure or renames the classes, it may be necessary to re-parameterize the XPATH and class references.**

</td></tr></table>

The script was tested on April 4th, 2023, and everything worked fine.

