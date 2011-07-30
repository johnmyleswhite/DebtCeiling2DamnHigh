import urllib2
import re

def load_url_data():
    f = open('urls.tsv', 'r')
    lines = f.readlines()
    f.close()
    data = map(lambda (l): l.strip().split("\t"), lines)
    url_data = {}
    for row in data:
        if not url_data.has_key(row[0]):
            url_data[row[0]] = {'HTMLMatch': row[1], 'URLMatch': row[2]}
    return url_data

def load_click_data():
    f = open('clicks.tsv', 'r')
    lines = f.readlines()
    f.close()
    click_data = map(lambda (l): l.strip().split("\t"), lines)
    return click_data

def add_to_url_data(url, url_data):
    url = url[0]
    if not url_data.has_key(url):
        url_data[url] = {}
        try:
            response = urllib2.urlopen(url)
            html = response.read()
            html_matches = html.find('debt')
            url_matches = url.find('debt')
            if html_matches < 0:
                url_data[url]['HTMLMatches'] = 0
            else:
                url_data[url]['HTMLMatches'] = 1
            if url_matches < 0:
                url_data[url]['URLMatches'] = 0
            else:
                url_data[url]['URLMatches'] = 1
        except:
            url_data[url] = {'HTMLMatches': 0, 'URLMatches': 0}
    return url_data

def add_to_click_data(url, click_data):
    click_data.append(url)
    return click_data

def write_url_data(url_data):
    f = open('urls.tsv', 'a')
    for url in url_data.keys():
        f.write("\t".join([url, str(url_data[url]['HTMLMatches']), str(url_data[url]['URLMatches'])]) + "\n")
    f.close()

def write_click_data(click_data):
    f = open('clicks.tsv', 'a')
    for url in click_data:
        f.write("\t".join(url) + "\n")
    f.close()

url_data = load_url_data()
click_data = load_click_data()

f = open('test_urls.csv', 'r')
lines = f.readlines()
f.close()
urls = map(lambda (l): l.strip().split(","), lines)
urls = urls[1:len(urls)]

urls = urls[0:9]

for url in urls:
    url_data = add_to_url_data(url, url_data)
    write_url_data(url_data)
    click_data = add_to_click_data(url, click_data)
    write_click_data(click_data)

