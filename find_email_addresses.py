# -*- coding: utf-8 -*-

"""
find_email_addresses.py

This tool gathers all the email addresses it can discover on a website,
and prints them in a list.

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

        #print()
        #print("VISITED LINKS:")
        #print(allLinks.sort())

        #print("EMAILS:")
        #print(allEmails.sort())
    except:
        print("Whoops! Caught an unhandled exception. This needs work... try a different URL!")

def visit(link, currentDepth, visitedLinks, foundEmails):
    """Attempts to open a new link, searching it for new emails and other parts of the site."""

    currentDepth += 1
    
    siteOpened = False
    if currentDepth < MAX_DEPTH:
    
        #print("Opening " + link)
        
        try:
            page = requests.get(link)
            siteOpened = True
        except:
            if currentDepth == 1:
                print("Oops, something went wrong with that URL! Please try a different URL.")
            else:
                print("DEBUG: Failed secondary link")
        
        if siteOpened:
        
            visitedLinks.append(link)
            soup = BeautifulSoup(page.text, "lxml")
            
            """Strain any emails out of this page's soup"""
            newEmails = getEmails(soup)
            for email in newEmails:
                if email not in foundEmails:
                    print(email)
                    foundEmails.append(email)

            """Skim any new links out of the soup, and visit each one"""
            newLinks = getLinks(soup, link, visitedLinks)
            for link in newLinks:
                if link not in visitedLinks:
                    newVisitedLinks, newFoundEmails = visit(link, currentDepth, visitedLinks, foundEmails)
                    visitedLinks.append(newVisitedLinks)
                    foundEmails.append(newFoundEmails)
    else:
        #print("DEBUG: Encountered Max Depth of " + str(MAX_DEPTH))
        pass
        
    return visitedLinks, foundEmails

    
def getEmails(someSoup):
    """This function takes a BeautifulSoup object and returns a list of any emails that were found"""
    
    newEmails = []
    
    mailtos = someSoup.select('a[href^=mailto]')
    
    for i in mailtos:
        if i != None:
            if re.match("[a-zA-Z]+[a-zA-Z0-9_.]*@[a-zA-Z0-9]+.[a-zA-Z]+", i.string) != None:
                newEmails.append(i.string)
    
    return newEmails

def getLinks(someSoup, currentSite, visitedLinks):
    """This function returns a set of potential links that are believed to be part of this site."""
    
    newLinks = []
    
    for elem in someSoup.find_all('a'):
        
        """...if that link is also "part of" this website..."""
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
        pass
        
    elif (len(hrefString) > 1) and (hrefString[0] == '/'):
        
        """avoid appending the same thing recursively"""
        suffix = False
        if hrefString == currentSite[-len(hrefString):]:
            suffix = True
        
        #for vlink in visitedLinks:
        #    if hrefString == vlink[-len(hrefString):]:
        #        suffix = True
        
        if suffix == False:
            partOfSite = True
            link = visitedLinks[0] + hrefString
            #print(link + " is part of site!")
    
    return partOfSite, link

if __name__ == "__main__":
    if len(sys.argv) > 1:
        find_email_addresses(sys.argv[1])
    else:
        print("No URL specified! Please enter python command as: 'find_email_addresses.py [URL]'")