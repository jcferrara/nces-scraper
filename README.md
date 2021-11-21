# Web Scraper for National Center for Education Statistics
*A web scraper built to download data en masse from the National Center for Education Statistics (NCES) (online college navigation tool)[https://nces.ed.gov/collegenavigator/]*

#### Methodology
Education data is collected from the web using the `beautifulsoup4` package. The scraper cycles through each of the 3,500+ degree-granting colleges in the United States to grab and store school metrics like total enrollment, address, faculty-to-student ratios, etc. In addition to descriptive data on colleges, data on 

1. **nces_scraper.py:** Customized web-scraping functions
2. **collect_school_data.py:** Uses the functions nces scraper functions to iterate through schools to collect data
3. **process_school_data.py:** Basic processing to demonstrate sample analyses to be completed with education data

#### Data collected
1. `school_code`
2. `school_address`
3. `school_zipcode`
4. `school_website`
5. `school_type`
6. `school_awards`
7. `school_campus_setting`
8. 
