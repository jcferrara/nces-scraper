# -*- coding: utf-8 -*-
"""

National Center for Education Statistics
Web Scraper School Statistics
Created by: Justin Ferrara

"""

import pandas as pd
from nces_scraper import get_schools, get_school_details, get_degree_counts

state_abbr_list = ['AL', 'AK', 'AZ', 'AR', 'CA', 'CO', 'CT', 'DE', 'FL', 'GA',
                    'HI', 'ID', 'IL', 'IN', 'IA', 'KS', 'KY', 'LA', 'ME', 'MD',
                    'MA', 'MI', 'MN', 'MS', 'MO', 'MT', 'NE', 'NV', 'NH', 'NJ',
                    'NM', 'NY', 'NC', 'ND', 'OH', 'OK', 'OR', 'PA', 'RI', 'SC',
                    'SD', 'TN', 'TX', 'UT', 'VT', 'VA', 'WA', 'WV', 'WI', 'WY',
                    'DC']

page_num_list = list(range(1, 31))

school_data = pd.DataFrame()

for state in state_abbr_list:

    for page in page_num_list:

        table = get_schools(state, page)
        school_data = pd.concat([school_data, table])

        print(state, page)

school_data.to_csv('schools.csv', index=False)

school_code = []
school_address = []
school_zipcode = []
school_website = []
school_type = []
school_awards = []
school_campus_setting = []
school_campus_housing = []
school_enrollment = []
school_student_to_faculty_ratio = []

num = 0

for s in school_data['school_link']:

    details = get_school_details(s)

    try:
        school_code.append(details['school_code'])
    except:
        school_code.append(999999)

    try:
        school_address.append(details['school_address'])
    except:
        school_address.append("None")

    try:
        school_zipcode.append(details['school_zipcode'])
    except:
        school_zipcode.append(999999)

    try:
        school_website.append(details['school_website'])
    except:
        school_website.append("None")

    try:
        school_type.append(details['school_type'])
    except:
        school_type.append("None")

    try:
        school_awards.append(details['school_awards'])
    except:
        school_awards.append("None")

    try:
        school_campus_setting.append(details['school_campus_setting'])
    except:
        school_campus_setting.append("None")

    try:
        school_campus_housing.append(details['school_campus_housing'])
    except:
        school_campus_housing.append("None")

    try:
        school_enrollment.append(details['school_enrollment'])
    except:
        school_enrollment.append(999999)

    try:
        school_student_to_faculty_ratio.append(details['school_student_to_faculty_ratio'])
    except:
        school_student_to_faculty_ratio.append(999999)

    num += 1
    print(num)


school_details = pd.DataFrame(list(zip(school_code, school_address, school_zipcode, school_website,
                            school_type, school_awards, school_campus_setting, school_campus_housing,
                            school_enrollment, school_student_to_faculty_ratio)),
                    columns = ['school_code', 'school_address', 'school_zipcode', 'school_website',
                                'school_type', 'school_awards', 'school_campus_setting', 'school_campus_housing',
                                'school_enrollment', 'school_student_to_faculty_ratio'])

school_details.to_csv('school_details.csv', index = False)

school_data = pd.read_csv('schools.csv')

degree_counts = pd.DataFrame()
num = 0

for link in school_data['school_link']:

    data = get_degree_counts(link)
    degree_counts = pd.concat([degree_counts, data])

    num += 1
    print(num)

degree_counts.to_csv('degree_counts.csv', index = False)
