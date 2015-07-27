#find_email_addresses.py
*"Sometimes it works!!"*

## Purpose
This tool will attempt to find any email addresses listed on the website it is provided, and print them to the screen.

This tool was written for and tested solely with Python 3.2, and the necessary libraries (lxml, requests, BeautifulSoup), which are included as well. This tool was developed on a machine running Windows 7.

## Known Bugs

* Is slow
* Sometimes seems like it's not going to finish
* Some exceptions are only being handled at top level, and causing early exit
* Cannot handle non-canonical URLs (requires correct URL be passed as argument)
* Cannot handle dynamic content added to DOM after initial HTTP response.
* Allowing duplicate email addresses to be printed
* Allowing incorrect email address formats to be printed

## Sample Output

```
C:\Users\Tom\Code\Email_Scraper_Poject>C:\Python32\python.exe find_email_addresses.py http://www.polygon.com
support@voxmedia.com
chris@polygon.com
justin@polygon.com
brian@polygon.com
susana@polygon.com
arthur@polygon.com
matt@polygon.com
mike@polygon.com
griffin@polygon.com
phil@polygon.com
danielle@polygon.com
nick@polygon.com
charlie@polygon.com
colin@polygon.com
samit@polygon.com
megan@polygon.com
dave@polygon.com
ben@polygon.com
owen@polygon.com
jake@polygon.com
sales@voxmedia.com
media@polygon.com
queries@polygon.com

C:\Users\Tom\Code\Email_Scraper_Poject>C:\Python32\python.exe find_email_addresses.py http://www.arstechnica.com
press@arstechnica.com
press@arstechnica.com
Andrew.hendler@arstechnica.com
Alexis_Moore@condenast.com
berkeley_gibson@condenast.com
Hayley_Samela@arstechnica.com

C:\Users\Tom\Code\Email_Scraper_Poject>C:\Python32\python.exe find_email_addresses.py http://www.spacex.com
media@spacex.com
sales@spacex.com

C:\Users\Tom\Code\Email_Scraper_Poject>C:\Python32\python.exe find_email_addresses.py http://www.eclipse.org
elections@eclipse.org.

C:\Users\Tom\Code\Email_Scraper_Poject>C:\Python32\python.exe find_email_addresses.py http://www.fivethirtyeight.com
contact@fivethirtyeight.com
datalab@fivethirtyeight.com
nrsilver@fivethirtyeight.com

C:\Users\Tom\Code\Email_Scraper_Poject>C:\Python32\python.exe find_email_addresses.py http://www.outdoors.org
amcinformation@outdoors.org
mladyzhensky@yahoo.com
lovejoyadm@aol.com
eoregan1@gmail.com
AMCbooks@outdoors.org
rburbank@outdoors.org
lhurley@outdoors.org
amclibrary@outdoors.org
AMCHR@outdoors.org
tolson@outdoors.org
AMClodging@outdoors.org
AMCPinkhamInfo@outdoors.org
amcyop@outdoors.org
amcvolservices@outdoors.org
AMCMembership@outdoors.org
AMCmembership@outdoors.org
Whoops! Caught an unhandled exception. This needs work... try a different URL!
```