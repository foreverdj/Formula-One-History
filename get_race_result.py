# -*- coding: UTF-8 -*-
from urllib import request
import chardet
from bs4 import BeautifulSoup

import csv

def get_race_result_url(year,gp='all'):
	#get url of specific/all gp from race2018.csv
	#return as list
	#get_race_result_url(2018, 'Belgium')
	#get_race_result_url(2018）
	results_table = []
	urls = []
	
	with open('./yearly_results/race%d.csv' %year, newline='') as f:
		reader = csv.reader(f, delimiter='\t')
		for row in reader:
			results_table.append(row)
	if gp == 'all':
		for i in range(1,len(results_table)):
			urls.append(results_table[i][9])
	else:
		for i in range(1,len(results_table)):
			if results_table[i][1] == gp:
				urls.append(results_table[i][9])
				break
			else:
				continue
	return urls

def get_race_result(year,gp):
	#get single race result for specific gp in one year
	#write into "./race_results/2018_Belgium.csv"
	#get_race_result(2018, 'Belgium')
	
	response_urls = get_race_result_url(year,gp)
	response = request.urlopen(response_urls[0])
	html = response.read()
	charset = chardet.detect(html)	#get encoding from html
	html = str(html.decode(charset["encoding"]))	#decode automatically
	soup = BeautifulSoup(html, 'lxml')
	response.close()
	
	with open("./race_results/%d_%s.csv" %(year,gp), "w+") as fp:
		tables = soup.findAll('table')
		tab = tables[0]
		header = ["Position", "No.", "First Name", "Last Name", "Abbr", "Car", "Laps", "Time/Retired", "Points"]
		fp.write(header[0])
		for h in range(1, 9):
			fp.write('\t' + header[h])
		fp.write('\n')
		for tr in tab.tbody.findAll('tr'):
			#fp.write("No %d Grand Prix:\t" %no_in_year)
			for td in tr.findAll('td'):
				text = td.getText().strip()
				if text == '':
					continue
				fp.write(text.replace('\n', '\t'))
				fp.write('\t')
			fp.write('\n')

get_race_result(2018, 'Belgium')