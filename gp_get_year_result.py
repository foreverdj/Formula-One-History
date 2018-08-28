# -*- coding: UTF-8 -*-
from urllib import request
import chardet
from bs4 import BeautifulSoup

def gp_get_year_result(selected_year):
	#get gp list for specific year
	#write into ./yearly_results/race2018.csv
	#gp_get_year_result(2018)
	host_url = 'https://www.formula1.com'
	url_1 = 'https://www.formula1.com/en/results.html/'
	url_2 = '/races.html'
	
	response_url = url_1 + str(selected_year) + url_2
	response = request.urlopen(response_url)
	html = response.read()
	charset = chardet.detect(html)	#get encoding from html
	html = str(html.decode(charset["encoding"]))	#decode automatically
	soup = BeautifulSoup(html, 'lxml')
	response.close()
	
	with open("./yearly_results/race%d.csv" %selected_year, "w+") as f:
		tables = soup.findAll('table')
		tab = tables[0]
		no_in_year = 1
		header = ["No.", "Grand Prix", "Date", "First Name", "Last Name", "Abbr", "Car", "Laps", "Time/Retired", "URL_race_result"]
		f.write(header[0])
		for h in range(1, 10):
			f.write('\t' + header[h])
		f.write('\n')
		for tr in tab.tbody.findAll('tr'):
			f.write("No %d Grand Prix:\t" %no_in_year)
			for td in tr.findAll('td'):
				text = td.getText().strip()
				if text == '':
					continue
				f.write(text.replace('\n', '\t'))
				f.write('\t')
			for td in tr.findAll('td'):
				for a in td.findAll('a'):
					f.write(host_url + a.get('href') + '\n')
			no_in_year+=1

