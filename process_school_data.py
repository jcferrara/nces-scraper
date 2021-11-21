#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Sep 18 12:07:10 2021

@author: JustinFerrara
"""

import pandas as pd
import numpy as np
import re

# Methodology: https://www.ice.gov/sites/default/files/documents/stem-list.pdf
degree_classifications = pd.read_csv('/Users/JustinFerrara/Desktop/NCES Scraper/degree_classifications.csv')
school_details = pd.read_csv('/Users/JustinFerrara/Desktop/NCES Scraper/school_details.csv')
degree_counts = pd.read_csv('/Users/JustinFerrara/Desktop/NCES Scraper/degree_counts.csv')
zip_codes = pd.read_csv('/Users/JustinFerrara/Desktop/NCES Scraper/us-zip-code-latitude-and-longitude.csv', delimiter=";", dtype={'Zip': 'str'})

degree_data = pd.merge(degree_counts, degree_classifications, how = "left", on = ['degree_name'])

school_details['school_enrollment'] = school_details['school_enrollment'].replace(999999, np.nan)

degree_data_agg = degree_data.groupby(['school_code', 'stem']).agg({'degree_count':'sum'}).reset_index()
degree_data_agg = degree_data_agg.pivot(index='school_code', columns='stem', values='degree_count').reset_index()
degree_data_agg = degree_data_agg.fillna(0)
degree_data_agg = degree_data_agg.rename(columns={"Yes": "stem_yes", "No": "stem_no"})

data = pd.merge(school_details, degree_data_agg, how = "left", on = "school_code")
data = pd.merge(data, zip_codes, how = "left", left_on = "school_zipcode", right_on = "Zip")

data['address_parts'] = data['school_address'].apply(lambda x: x.split(","))

city_list = []
state_list = []

for i in range(len(data['City'])):
    if pd.isnull(data['City'][i]):  
        try:
            city_list.append(data['address_parts'][i][1].strip())
            state_list.append(data['address_parts'][i][2].strip())
        except:
            city_list.append(np.nan)
            state_list.append(np.nan)
    else:
        city_list.append(data['City'][i])
        state_list.append(data['State'][i])

data['school_city'] = city_list
data['school_state'] = state_list

data = data[['school_zipcode', 'school_enrollment', 'stem_no', 'stem_yes', 'school_city', 'school_state']]

# Aggregate data by zip code
data_agg_zip = data.groupby(['school_zipcode']).agg({'stem_yes':'sum', 'stem_no':'sum', 'school_enrollment':'sum'}).reset_index()
data_agg_zip['stem_perc'] = data_agg_zip['stem_yes']/(data_agg_zip['stem_no'] + data_agg_zip['stem_yes'])

# Aggregate data by city-state
data_agg_city = data.groupby(['school_city', 'school_state']).agg({'stem_yes':'sum', 'stem_no':'sum', 'school_enrollment':'sum'}).reset_index()
data_agg_city['stem_perc'] = data_agg_city['stem_yes']/(data_agg_city['stem_no'] + data_agg_city['stem_yes'])

# Aggregate data by state
data_agg_state = data.groupby(['school_state']).agg({'stem_yes':'sum', 'stem_no':'sum', 'school_enrollment':'sum'}).reset_index()

us_states = {
	'Alabama': 'AL',
	'Alaska': 'AK',
	'Arizona': 'AZ',
	'Arkansas': 'AR',
	'California': 'CA',
	'Colorado': 'CO',
	'Connecticut': 'CT',
	'Delaware': 'DE',
	'District of Columbia': 'DC',
	'Florida': 'FL',
	'Georgia': 'GA',
	'Hawaii': 'HI',
	'Idaho': 'ID',
	'Illinois': 'IL',
	'Indiana': 'IN',
	'Iowa': 'IA',
	'Kansas': 'KS',
	'Kentucky': 'KY',
	'Louisiana': 'LA',
	'Maine': 'ME',
	'Maryland': 'MD',
	'Massachusetts': 'MA',
	'Michigan': 'MI',
	'Minnesota': 'MN',
	'Mississippi': 'MS',
	'Missouri': 'MO',
	'Montana': 'MT',
	'Nebraska': 'NE',
	'Nevada': 'NV',
	'New Hampshire': 'NH',
	'New Jersey': 'NJ',
	'New Mexico': 'NM',
	'New York': 'NY',
	'North Carolina': 'NC',
	'North Dakota': 'ND',
	'Ohio': 'OH',
	'Oklahoma': 'OK',
	'Oregon': 'OR',
	'Pennsylvania': 'PA',
	'Rhode Island': 'RI',
	'South Carolina': 'SC',
	'South Dakota': 'SD',
	'Tennessee': 'TN',
	'Texas': 'TX',
	'Utah': 'UT',
	'Vermont': 'VT',
	'Virginia': 'VA',
	'Washington': 'WA',
	'West Virginia': 'WV',
	'Wisconsin': 'WI',
	'Wyoming': 'WY'
}

state_name = []

for st in data_agg_state['school_state']:
    
    if len(st) == 2:
        state_name.append(st)
    else:
        digit_index = re.search(r"\d", st)
        try:
            filter_index = int(digit_index.span()[0])-1
            state_abbr = st[0:filter_index]
            state_abbr = us_states[state_abbr]
            state_name.append(state_abbr)
        except:
            state_name.append("NAN")

data_agg_state['state_name'] = state_name
data_agg_state = data_agg_state.groupby(['state_name']).agg({'stem_yes':'sum', 'stem_no':'sum', 'school_enrollment':'sum'}).reset_index()
data_agg_state['stem_perc'] = data_agg_state['stem_yes']/(data_agg_state['stem_no'] + data_agg_state['stem_yes'])

data_agg_state.to_csv('/Users/JustinFerrara/Desktop/NCES Scraper/stem_percent_by_state.csv', index = False)





