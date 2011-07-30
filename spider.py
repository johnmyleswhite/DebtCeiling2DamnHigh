import urllib2
import re

f = open('test_urls.txt', 'r')
lines = f.readlines()
f.close()

urls = map(lambda (l): l.strip(), lines)

#urls = ['http://www.nasa.gov', 'http://www.whitehouse.gov']

#p = re.compile('debt', re.IGNORECASE)

for url in urls:
    response = urllib2.urlopen(url)
    html = response.read()
    html_matches = html.find('debt')
    url_matches = url.find('debt')
    if html_matches < 0:
        if url_matches < 0:
            print url + "\t" + str(0) + "\t" + str(0)
        else:
            print url + "\t" + str(0) + "\t" + str(1)
    else:
        if url_matches < 0:
            print url + "\t" + str(1) + "\t" + str(0)
        else:
            print url + "\t" + str(1) + "\t" + str(1)
