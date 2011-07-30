#!/usr/bin/env python
# encoding: utf-8
"""
agency_stream.py

Description: 

Created by Drew Conway (drew.conway@nyu.edu) on 2011-07-29 
# Copyright (c) 2011, under the Simplified BSD License.  
# For more information on FreeBSD see: http://www.opensource.org/licenses/bsd-license.php
# All rights reserved.
"""

import sys
import os
import csv
import json

def parse_1usa(json_line):
	"""docstring for parse_1usa"""
	try:
		l = json.loads(json_line)
		return {'url' : l['u'], 't' : l['t'], 'hc' : l['hc']}
	except ValueError:
		return {'url' : '', 't' : '', 'hc' : ''}
		
def find_top_level(url):
	"""docstring for topLevel"""
	domains = url.split('.')[1:-1]
	
	is_domain = map(lambda t: t.find('/') < 0, domains)
	top_levels = [(domains[i]) for (i) in xrange(len(domains)) if is_domain[i]]
	if len(top_levels) < 1:
		pass
	else:
		if len(top_levels) > 1:
			return (top_levels[1], url)
		else:
			return (top_levels[0], url)
	

def main():
	
	usa1_file = open('data/usagov_bitly_data2011-07-29-1311980388.txt', 'r')
	usa1_parse = map(parse_1usa, usa1_file.readlines())
	
	dict_writer = csv.DictWriter(open("data/test_urls.csv", "w"), fieldnames=usa1_parse[0].keys())
	dict_writer.writeheader()
	for r in usa1_parse:
		dict_writer.writerow(r)
	
	


if __name__ == '__main__':
	main()

