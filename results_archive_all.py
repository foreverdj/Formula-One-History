# -*- coding: UTF-8 -*-
#get all gp lists from 1950 till 2018
from gp_get_year_result import gp_get_year_result

years = list(range(1950, 2019))	#till 2018
for selected_year in years:
	gp_get_year_result(selected_year)