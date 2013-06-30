# KeywordGrabber Parser
# Varun Naik 2013
################################################################################

import urllib2
from bs4 import BeautifulSoup
import re

# urls: List of strings. Each string is a URL to parse.
urls = []
containers = []
ignoredwords = []

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

def parseselectors(selectors):
    """Given a list of selectors, add them into selectorlist by type"""
    selectorlist = {tag: [], id: [], classname: []}
    
    for s in selectors:
        if s[0] == '.':
            selectorlist.classname.append(s[1:])
        elif s[0] == '#':
            selectorlist.id.append(s[1:])
        else:
            selectorlist.name.append(s)
            
    return selectorlist
    
url = None
# Open Input file
for line in open('urls.conf'):
    if line.startswith("#"):
        continue # Ignore comments

    line = line.strip()
    
    if len(line) == 0: 
        continue # Ignore blank lines
    
    # If the line has selectors get them
    if line.lower().startswith("selector:"):
        selectors = parseselectors(line.split(":")[1].split(','))
    else:
        if url:
           # Process URL on line and append it to the list of URLs
           urls.extend([{'url': u, 'selectors': selectors} for u in expandurls([url], pattern)])
           selector = None
           url = None
        
        # Otherwise save the URL and look for a Selector line below and before the next URL   
        url = line
        pattern =  re.findall('<([0-9a-z\-]*)>', line)

# Process the last line too
if url:
    urls.extend([{'url': u, 'selectors': selectors} for u in expandurls([url], pattern)])
    
    
# Read all ignored words into list
for line in open('ignored.conf'):
    if line.startswith('#'):
        continue

    line = line.strip()
    if len(line) == 0: continue # Skip blank lines

    ignoredwords.append(line)

def visible(element):
    content = unicode(element)
    if element.parent.name in ['style', 'script', '[document]', 'head', 'title']:
        return False
    elif re.match('<!--.*-->', content):
        return False
    elif content.isspace():
        return False
    return True
      
# Load each URL
for url in urls:
   
    soup = BeautifulSoup(urllib2.urlopen(url['url']))
    selectors = url['selectors']
    if selector == None:
        texts = soup.findAll(text=True)
    elif selector[0] == '.':
        print selector.split('.')[1]
        texts = soup.findAll(class_=selector.split('.')[1], text=True)
    elif selector[0] == '#':
        texts = soup.findAll(id=selector.split('#')[1], text=True)
    else: # Selector is tagname
        texts = soup.findAll(selector, text=True)
    visible_texts = filter(visible, texts)
    print visible_texts
    # Use selectors if specified to get all groups of words
    # Count each group of words
    # Count each word
    # Emit counts array as csv
    
    

# Process it and store results into array

# Sort results array

# Write results array to files
