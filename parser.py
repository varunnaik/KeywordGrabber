# KeywordGrabber Parser
# Varun Naik 2013
################################################################################

import urllib2
from BeautifulSoup import BeautifulSoup
import re

# urls: List of strings. Each string is a URL to parse.
urls = []

def expandurls(urllist, regexlist):
    # Parse the URL and expand any wildcards; return a list of URLs
    
    # This is a little hard because a single URL may have multiple wildcards
    # The solution is to parse all urls, replacing one wildcard with
    # all expansions and then calling the function recursively to replace
    # all other wildcards in that URL
    if len(regexlist) == 0:
        return urllist

    expandedurls = []
    
    regex = regexlist[0]
    start, end = regex.split('-')

    if type(start) is int:
        for i in xrange(start, end+1):
            for url in urllist:
                expandedurls.append(url.replace('<'+regex+'>', str(i)))
    else:
        for i in xrange(ord(start), ord(end)+1):
            for url in urllist:
                expandedurls.append(url.replace('<'+regex+'>', chr(i)))

    return expandurls(expandedurls, regexlist[1:])


# Open Input file
for line in open('in.conf'):
    if line.startswith("#"):
        continuen
    pattern =  re.findall('<([0-9a-z\-]*)>', line)

    # Process URL on line and append it to the list of URLs
    urls.append(expandurls([line], pattern))


# Read all ignored words into list

# Read containers to search into list

# Process and expand URLs

# Load each URL

# Process it and store results into array

# Sort results array

# Write results array to files
