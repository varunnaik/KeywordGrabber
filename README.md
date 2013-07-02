KeywordGrabber
==============

Python Webscraper that gets the count of words and phrases on a page or set of pages. Provides results as a CSV file.

Usage:
1. In urls.conf, specify the URLs to crawl, one per line.
2. In the same file, optionally specify the HTML selectors to use below each URL, separated by commas. Prefix the line with 'Selectors:' See urls.conf for examples. All selectors will be used when searching, for example, 'div, .content' will match dics with class .content and ignore any other element with .content.
2. For each URL, you can specify wildcard characters in each URL. Wildcards allowed: <a-z>, <0-9> - where each wildcard is substituted with the range of characters. Example: example.com/page-<89-102> will be replaced with example.com/page-89, example.com/page-90, ... example.com/page-102 and each URL will be loaded and parsed.
3. Ignored words present in ignore.conf will be dropped from the CSV. One word or phrase per line.

Output:
Output will be in two CSV files, phrases.csv and words.csv
They contain the words and phrases, respectively, in descending order of occurence, along with their counts.

Future Enhancements:
1. Ignoring phrases
2. More sophisticated selectors and maybe deselectors