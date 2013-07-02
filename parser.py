# KeywordGrabber Parser
# Varun Naik 2013
################################################################################

import urllib2
from bs4 import BeautifulSoup
import re
from collections import defaultdict
import operator
import sets
import codecs

# urls: List of strings. Each string is a URL to parse.
urls = []
ignoredwords = []
ignoredphrases = []
phraselist = defaultdict(int)
wordlist = defaultdict(int)

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
    selectorlist = {'tag': [], 'id': [], 'classname': []}
    
    for s in selectors:
        if s[0] == '.':
            selectorlist['classname'].append(s[1:])
        elif s[0] == '#':
            selectorlist['id'].append(s[1:])
        else:
            selectorlist['tag'].append(s)
            
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
    
    # Append to wordlist or phraselist depending on whether it is a word or a phrase
    if len(line.split()) == 1:
        ignoredwords.append(line)
    else:
        ignoredphrases.append(line)


ignoredwords = sets.ImmutableSet(ignoredwords)
ignoredphrases = sets.ImmutableSet(ignoredphrases)

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
    
    print "Opening", url['url'],
   
    soup = BeautifulSoup(urllib2.urlopen(url['url']))
    selectors = url['selectors']
    visible_texts = []

    for tag in soup.findAll(selectors['tag'], attrs={"class": selectors['classname'], "id": selectors['id']}):
         if visible(tag):        
            texts = tag.findAll(text=True)
            visible_texts.extend(filter(visible,texts))
    
    for text in visible_texts:
        words = text.split()
        
        for word in words:
            word = word.lower().replace(",","")
            if word in ignoredwords: continue
            wordlist[word] += 1
        
        if text in ignoredphrases: continue 
        phraselist[text.strip().lower().replace(",","")] += 1
    print " : ", "done"
         
print "Got", len(wordlist), "words and", len(phraselist), "phrases."
wordlist = sorted(wordlist.iteritems(), key=operator.itemgetter(1))[::-1]
phraselist = sorted(phraselist.iteritems(), key=operator.itemgetter(1))[::-1]

word_csv = codecs.open('words.csv','w','UTF-8')
for word in wordlist:
    word_csv.write(word[0]+','+unicode(word[1])+'\n')
word_csv.close()
    
phrase_csv = codecs.open('phrases.csv','w','UTF-8')
for phrase in phraselist:
    phrase_csv.write(phrase[0]+','+unicode(phrase[1])+'\n')
phrase_csv.close()
    
print "Output files words.csv and phrases.csv written, run completed."