KeywordGrabber
==============

Python Webscraper that gets the count of words and phrases on a page or set of pages. Provides results as a CSV file.

Usage:
1. In in.conf, specify the URLs to crawl, one per line.
2. Wildcards allowed: <a-z>, <0-9> - where each wildcard is substituted with the range of characters. Example: example.com/page-<89-102> will be replaced with example.com/page-89, example.com/page-90, ... example.com/page-102 and each URL will be loaded and parsed.
3. Ignored words present in ignore.conf will be dropped. One word per line.

Output:
Output will be in two CSV files, phrases.csv and words.csv
They contain the words and phrases, respectively, in descending order of occurence, along with their counts.

Future Enhancements:
1. Create parser.conf
2. Add support for skipping parts of page based on tag or getting parts of page based on tag
