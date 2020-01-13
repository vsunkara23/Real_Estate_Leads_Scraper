Real_Estate_Leads_Scraper
=======

- [Overview](#Overview)
- [Setup](#Setup)
    - [Prerequisites](#Prerequisites)
    - [Background](#Background)
    - [Running Program](#Running-Program)
- [Output](#Output)

Overview
------

### Goal:

Developing a core web scraping application to find high-quality leads or Real Estate data of ongoing construction projects in Indian Market for Greenway Building Materials India Pvt. Ltd., a building materials company. 

### Problem: 
1) Time wasted on manually searching and filling details of leads in excel sheet.
2) Some leads don't have enough details such as contact information like phone number and website.
3) Lack of proper information about leads slows down business.
4) Money wasted on time-consuming employee search for quality leads.

### Solution:
1) Web scraper to automate process of finding leads and filling details into excel sheet programmatically.
2) Filtering results from scraping for high quality leads only that satisfy all required information criteria in excel sheet.
3) Thousands of leads within minutes.

### Program Specifics:
1) User defines city on the terminal. All possible matches of ongoing construction projects are scraped from the following website: https://www.commonfloor.com/project-search?city=(user-defined-string).

2) Filtered by only matches that had complete information such as company name and address.

2) Queried Google Places API and parsed returned JSON to get additional leads information such as company website and phone number.

3) Wrote leads data collected from website and Google Places API to CSV file.


___Required Information Criteria For High Quality-Leads:___
1) Project Name
2) Company Name
3) Location
4) Phone Number
5) Website 


Setup
------

### Prerequisites

Python 3       

Beautiful Soup      (pip install beautifulsoup4)

Requests Library    (pip install requests)

### Background

This program is run on terminal. 
The user keeps querying the program for more ongoing construction projects leads from their desired cities until they input "No" and user finishes querying.
Once user is done querying, program outputs an excel sheet consisting of a list of scraped ongoing construction projects with details.
Below is a demonstration of how the program is run on terminal.

### Running Program

<a href="https://asciinema.org/a/291902?autoplay=1"><img src="https://asciinema.org/a/291902.png" width="836"/></a>

Output
------
Generated output from running program.

![](images/output_img.png?raw=true)

