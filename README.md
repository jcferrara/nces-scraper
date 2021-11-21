# Web Scraper for National Center for Education Statistics
*A web scraper built to download data en masse from the National Center for Education Statistics (NCES) online college navigation tool*

#### Methodology
Education data is collected from the web using the `beautifulsoup4` package. The scraper cycles through each of the 3,500+ degree-granting colleges in the United States to grab and store school metrics like total enrollment, address, faculty-to-student ratios, etc. In addition to descriptive data on colleges, data on 

1. **nces_scraper.py:** Customized web-scraping functions
2. **Text:** Uses the functions available in `nces_scraper.py` to iterate through schools to collect data
3. **process:** Basic processing to demonstrate sample analyses to be completed with education data

#### Data collected
Text
