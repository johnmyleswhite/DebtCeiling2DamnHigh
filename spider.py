import urllib2
import re
import csv

def load_url_data():
    f = open('urls.tsv', 'r')
    lines = f.readlines()
    f.close()
    data = map(lambda (l): l.strip().split("\t"), lines)
    url_data = {}
    for row in data:
        if not url_data.has_key(row[0]):
            url_data[row[0]] = {'HTMLMatches': row[1], 'URLMatches': row[2]}
    return url_data

def reader(l):
    row = l.strip().split("\t")
    return {'url': row[0], 'hc': row[1], 't': row[2]}

def load_click_data():
    f = open('clicks.tsv', 'r')
    lines = f.readlines()
    f.close()
    click_data = map(reader, lines)
    return click_data

def add_to_url_data(url, url_data):
    url = url['url']
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
    f = open('urls.tsv', 'w')
    for url in url_data.keys():
        f.write("\t".join([url, str(url_data[url]['HTMLMatches']), str(url_data[url]['URLMatches'])]) + "\n")
    f.close()

def write_click_data(click_data):
    f = open('clicks.tsv', 'w')
    for url in click_data:
        f.write("\t".join([url['url'], url['hc'], url['t']]) + "\n")
    f.close()

url_data = load_url_data()
click_data = load_click_data()

csv_reader = csv.DictReader(open('test_urls.csv', 'r'), fieldnames = ['url', 'hc', 't']) #has_header = True)
urls = map(lambda r: r, csv_reader)
urls = urls[1:len(urls)]

for url in urls:
    url_data = add_to_url_data(url, url_data)
    write_url_data(url_data)
    click_data = add_to_click_data(url, click_data)
    write_click_data(click_data)

