# -*- coding: utf-8 -*-
"""

National Center for Education Statistics
Web Scraper School Statistics
Created by: Justin Ferrara

"""

import pandas as pd
import requests
from bs4 import BeautifulSoup
import re


def get_schools(state_abbr, page_num):

    url = 'https://nces.ed.gov/collegenavigator/?s=' + str(state_abbr) + '&l=92+93&pg=' + str(page_num)

    result = requests.get(url)
    soup = BeautifulSoup(result.content, features="lxml")

    html = soup.find('table', attrs = {'id':'ctl00_cphCollegeNavBody_ucResultsMain_tblResults'})

    white_rows = html.findAll('tr', attrs = {'class':'resultsW'})
    yellow_rows = html.findAll('tr', attrs = {'class':'resultsY'})

    school_links = []
    school_name = []
    school_code = []

    for w in white_rows:

        link = w.findAll('a', href=True)[0]["href"]
        school_links.append(link)
        school_code.append(int(link[len(link)-6:len(link)]))
        school_name.append(w.find('strong').text)

    for y in yellow_rows:

        link = y.findAll('a', href=True)[0]["href"]
        school_links.append(link)
        school_code.append(int(link[len(link)-6:len(link)]))
        school_name.append(y.find('strong').text)

    data = pd.DataFrame(list(zip(school_name, school_links, school_code)),
                        columns = ['school_name', 'school_link', 'school_code'])

    data['school_state'] = state_abbr

    return(data)


def get_school_details(school_link):
    
    info_dict = {}
    
    info_dict['school_code'] = int(school_link[len(school_link)-6:len(school_link)])
    
    url = 'https://nces.ed.gov/collegenavigator/' + str(school_link)
    
    result = requests.get(url)
    soup = BeautifulSoup(result.content, features="lxml")
    
    school_address = str(soup.find('span', attrs = {'style':'position:relative'}).contents[2])
    info_dict['school_address'] = school_address
    
    try:
        school_zipcode = school_address[len(school_address)-5:]
        find_zip = r'(\d{5}\-?\d{0,4})'
        school_zipcode = re.search(find_zip, school_address).group(0)
    except:
        school_zipcode = "None"
    
    if '-' in school_zipcode:
        end_index = school_zipcode.find('-')
        school_zipcode = school_zipcode[0:end_index]
        
    info_dict['school_zipcode'] = school_zipcode
    
    html = soup.find('table', attrs = {'class':'layouttab'})
    
    for i in html.findAll('tr'):
            
        row_title = str(i.contents[0].text)
        row_value = str(i.contents[1].text)
        
        if 'Website' in row_title:
            info_dict['school_website'] = row_value
        elif 'Type' in row_title:
            info_dict['school_type'] = row_value
        elif 'Awards' in row_title:
            info_dict['school_awards'] = row_value
        elif 'Campus setting' in row_title:
            info_dict['school_campus_setting'] = row_value
        elif 'Campus housing' in row_title:
            info_dict['school_campus_housing'] = row_value
        elif 'population' in row_title:
            end_index = row_value.find('(')
            if end_index != -1:
                row_value = row_value[0:end_index-1].strip()
            row_value = int(row_value.replace(",", ""))
            info_dict['school_enrollment'] = row_value
        elif 'faculty' in row_title:
            end_index = row_value.find('to')
            if end_index != -1:
               row_value = row_value[0:end_index-1].strip()
            row_value = int(row_value.replace(",", ""))
            info_dict['school_student_to_faculty_ratio'] = row_value

    return(info_dict)


def get_degree_counts(school_link):
    
    url = 'https://nces.ed.gov/collegenavigator/' + str(school_link) + '#programs'
    
    school_code = int(school_link[len(school_link)-6:len(school_link)])
    
    result = requests.get(url)
    soup = BeautifulSoup(result.content, features="lxml")
    
    degrees = soup.find('table', attrs = {'class':'pmtabular'})
    
    degree_name_list = []
    degree_count_list = []
    
    for d in degrees.findAll('tr', attrs = {'class':'level1indent'}):
        
        levels = len(d)
        
        degree_name = d.contents[0].text
        
        if levels == 2:
            count1 = d.contents[1].text.replace("-", "0").replace(",", "").replace("d", "")
            degree_count = int(count1)
        elif levels == 3:
            count1 = d.contents[1].text.replace("-", "0").replace(",", "").replace("d", "")
            count2 = d.contents[2].text.replace("-", "0").replace(",", "").replace("d", "")
            degree_count = int(count1) + int(count2)
        elif levels == 4:
            count1 = d.contents[1].text.replace("-", "0").replace(",", "").replace("d", "")
            count2 = d.contents[2].text.replace("-", "0").replace(",", "").replace("d", "")
            count3 = d.contents[3].text.replace("-", "0").replace(",", "").replace("d", "")
            degree_count = int(count1) + int(count2) + int(count3)
        elif levels == 5:
            count1 = d.contents[1].text.replace("-", "0").replace(",", "").replace("d", "")
            count2 = d.contents[2].text.replace("-", "0").replace(",", "").replace("d", "")
            count3 = d.contents[3].text.replace("-", "0").replace(",", "").replace("d", "")
            count4 = d.contents[4].text.replace("-", "0").replace(",", "").replace("d", "")
            degree_count = int(count1) + int(count2) + int(count3) + int(count4)
        elif levels == 6:
            count1 = d.contents[1].text.replace("-", "0").replace(",", "").replace("d", "")
            count2 = d.contents[2].text.replace("-", "0").replace(",", "").replace("d", "")
            count3 = d.contents[3].text.replace("-", "0").replace(",", "").replace("d", "")
            count4 = d.contents[4].text.replace("-", "0").replace(",", "").replace("d", "")
            count5 = d.contents[5].text.replace("-", "0").replace(",", "").replace("d", "")
            degree_count = int(count1) + int(count2) + int(count3) + int(count4) + int(count5)
        else:
            count1 = d.contents[1].text.replace("-", "0").replace(",", "").replace("d", "")
            count2 = d.contents[2].text.replace("-", "0").replace(",", "").replace("d", "")
            count3 = d.contents[3].text.replace("-", "0").replace(",", "").replace("d", "")
            count4 = d.contents[4].text.replace("-", "0").replace(",", "").replace("d", "")
            count5 = d.contents[5].text.replace("-", "0").replace(",", "").replace("d", "")
            count6 = d.contents[6].text.replace("-", "0").replace(",", "").replace("d", "")
            degree_count = int(count1) + int(count2) + int(count3) + int(count4) + int(count5) + int(count6)
                
        degree_name_list.append(degree_name)
        degree_count_list.append(degree_count)
        
    data = pd.DataFrame(list(zip(degree_name_list, degree_count_list)), 
                        columns = ['degree_name', 'degree_count'])
    
    data['school_code'] = school_code
    
    return(data)