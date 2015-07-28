# -*- coding: utf-8 -*-

"""
find_email_addresses.py

This tool gathers all the email addresses it can discover on a website,
and prints them in a list.

TODO 1  fix get_emails to find emails anywhere, not just mailtos

TODO 2  make get_links hungrier to traverse more than single relative links
        (absolute links, multiple layers of relative links, query params...)
        and design a smarter safety against runaway traversal
        
TODO 3  provide a better user experience (real time feedback, timeouts, URL resolution)        

Author: Tom Morris
Soundtrack: Deadmau5 - Get Scraped (2005)
"""

import sys
import requests
from lxml import html
from bs4  import BeautifulSoup
import re

MAX_DEPTH = 5

def find_email_addresses(url):
    """Print all the email addresses discoverable at the given URL."""

    try:
        currentDepth = 0
        allLinks = []
        allEmails = []
            
        allLinks, allEmails = visit(url, currentDepth, allLinks, allEmails)

    except:
        print("Whoops! Caught an unhandled exception. This needs work... try a different URL!")

def visit(link, currentDepth, visitedLinks, foundEmails):
    """Attempts to open a new link, searching it for new emails and other parts of the site."""

    """Use current depth as a quick and dirty backstop against runaway traversal."""
    currentDepth += 1
    if currentDepth > MAX_DEPTH:
        return visitedLinks, foundEmails

    try:
        page = requests.get(link)
    except:
        if currentDepth == 1:
            print("Oops, something went wrong with that URL! Please try a different URL.")
        else:
            return visitedLinks, foundEmails
    
    visitedLinks.append(link)
    soup = BeautifulSoup(page.text, "lxml")
    
    """Strain any emails out of this page's soup"""
    newEmails = get_emails(soup)
    for email in newEmails:
        if email not in foundEmails:
            print(email)
            foundEmails.append(email)

    """Skim any new links out of the soup, and visit each one"""
    newLinks = get_links(soup, link, visitedLinks)
    for link in newLinks:
        if link not in visitedLinks:
            newVisitedLinks, newFoundEmails = visit(link, currentDepth, visitedLinks, foundEmails)
            visitedLinks.append(newVisitedLinks)
            foundEmails.append(newFoundEmails)
        
    return visitedLinks, foundEmails

    
def get_emails(someSoup):
    """This function takes a BeautifulSoup object and returns a list of any emails that were found"""
    
    newEmails = []
    
    mailtos = someSoup.select('a[href^=mailto]')
    
    for i in mailtos:
        if i != None:
            if re.match("[a-zA-Z]+[a-zA-Z0-9_.]*@[a-zA-Z0-9]+.[a-zA-Z]+", i.string) != None:
                newEmails.append(i.string)
    
    return newEmails

def get_links(someSoup, currentSite, visitedLinks):
    """This function returns a set of potential links that are believed to be part of this site."""
    
    newLinks = []
    
    for elem in someSoup.find_all('a'):
        
        """Figure out whether it's 'part of' this site."""
        validLink, link = is_link_part_of_site(currentSite, elem, visitedLinks)
        
        if validLink and link not in visitedLinks:
            newLinks.append(link)

    return newLinks

def is_link_part_of_site(currentSite, linkElem, visitedLinks):
    """Tries to determine if this link should be considered part of the current website, and therefore visited."""
    
    partOfSite = False
    link = ""
    
    hrefString = linkElem.get('href');
    if hrefString == None:
        return partOfSite, link
    
    """build an absolute link from relative links"""
    if (len(hrefString) > 1) and (hrefString[0] == '/'):
        
        """avoid appending the same thing recursively"""
        suffix = False
        if hrefString == currentSite[-len(hrefString):]:
            suffix = True
        
        if suffix == False:
            partOfSite = True
            link = visitedLinks[0] + hrefString
    
    return partOfSite, link

if __name__ == "__main__":
    if len(sys.argv) > 1:
        find_email_addresses(sys.argv[1])
    else:
        print("No URL specified! Please enter python command as: 'find_email_addresses.py [URL]'")