from __future__ import print_function
from bs4 import BeautifulSoup
import requests
import urllib
import xlwt
import sys
import re
import itertools
import json

wb = xlwt.Workbook(encoding="utf-8")

data_sheet = wb.add_sheet("Leads")

data_sheet.write(0, 0, "S.NO", style = xlwt.easyxf('font: bold 1; border: top medium, right medium, bottom medium, left medium;'))
data_sheet.write(0, 1, "Project", style = xlwt.easyxf('font: bold 1; border: top medium, right medium, bottom medium, left medium;'))
data_sheet.write(0, 2, "Company", style = xlwt.easyxf('font: bold 1; border: top medium, right medium, bottom medium, left medium;'))
data_sheet.write(0, 3, "Location", style = xlwt.easyxf('font: bold 1; border: top medium, right medium, bottom medium, left medium;'))
data_sheet.write(0, 4, "Phone No.", style = xlwt.easyxf('font: bold 1; border: top medium, right medium, bottom medium, left medium;'))
data_sheet.write(0, 5, "Website", style = xlwt.easyxf('font: bold 1; border: top medium, right medium, bottom medium, left medium;'))

def place_details_API(str):
	endpoint_url = "https://maps.googleapis.com/maps/api/place/details/json?"
	info_string = str
	api_key = "PUT-API-KEY-HERE"
	params = {
		'place_id': info_string,
		'key': api_key,
	}
	res = requests.get(endpoint_url, params = params)
	json_data = json.loads(res.content)
	contact_list = []
	if 'website' in json_data['result']:
		contact_list = [(json_data['result']['website'])]
		if 'international_phone_number' in json_data['result']:
			contact_list.append((json_data['result']['international_phone_number']))
			return contact_list
		else:
			contact_list.append("NA")
			return contact_list
	elif 'website' not in json_data['result']:
		contact_list = ["NA"]
		if 'international_phone_number' in json_data['result']:
			contact_list.append((json_data['result']['international_phone_number']))
			return contact_list
		else:
			contact_list.append("NA")
			return contact_list

def place_search_API(str):
	str = str[:-1:]
	str = str + " india"
	endpoint_url = "https://maps.googleapis.com/maps/api/place/findplacefromtext/json?"
	info_string = urllib.parse.quote_plus(str)
	api_key = "PUT-API-KEY-HERE"
	params = {
		'input': info_string,
		'inputtype': "textquery",
		'key': api_key,
	}
	res = requests.get(endpoint_url, params = params)
	results = json.loads(res.content)
	contact_list = []
	if results['candidates'] != []: 
		place_id = results['candidates'][0]['place_id']
		contact_list = place_details_API(str = place_id)
		return contact_list
	else:
		contact_list = ["NA", "NA"]
		return contact_list

def scrape_func(str):
	url = "https://www.commonfloor.com/project-search?city=" + str
	html_content = requests.get(url).text
	soup = BeautifulSoup(html_content, "lxml")

	invalid_request = soup.find("div", {"class":"paplink md"})
	if invalid_request:
		print("No leads found. Try another city.")
		sys.exit()
	project_listings = soup.find_all("h2")
	company_info = soup.find_all("h4")
	i = 0
	global row
	contact_list = []
	while i < len(company_info):
		name_of_company = ""    
		location_of_company = ""
		if "By" in company_info[i].text:
			rmv_by = re.compile('(\s*)By(\s*)')
			words = rmv_by.sub('', company_info[i].text)
			words = words.split(" ") 
			for substring in words:
				if substring == "in":
					break;
				else:
					name_of_company += substring
					name_of_company += " "
			contact_list = place_search_API(str = name_of_company)
			index = 0
			bool_val = 0
			while index < len(words):
				if words[index] == "in":
					bool_val = 1
				elif bool_val == 1:
					location_of_company += words[index] 
					location_of_company += " "
				index += 1
			location_of_company = location_of_company[:-1:]
			location_of_company += ", "
			location_of_company += str.capitalize()  
			if "NA" not in contact_list:
				data_sheet.write(row, 0, row, style = xlwt.easyxf('border: top thin, right thin, bottom thin, left thin;'))	
				data_sheet.write(row, 1, project_listings[i].text, style = xlwt.easyxf('border: top thin, right thin, bottom thin, left thin;'))		
				data_sheet.write(row, 2, name_of_company, style = xlwt.easyxf('border: top thin, right thin, bottom thin, left thin;'))			
				data_sheet.write(row, 3, location_of_company, style = xlwt.easyxf('border: top thin, right thin, bottom thin, left thin;'))			
				data_sheet.write(row, 4, contact_list[1], style = xlwt.easyxf('border: top thin, right thin, bottom thin, left thin;'))
				data_sheet.write(row, 5, contact_list[0], style = xlwt.easyxf('border: top thin, right thin, bottom thin, left thin;'))
				row += 1
		i += 1
	col_width = 256 * 50                     
	try:
		for i in itertools.count():
			if i > 0:
				data_sheet.col(i).width = col_width
	except ValueError:
		pass

def main():
	print("\nWhich city do you want to scrape leads from?\n(Example: 'Bangalore', 'Mumbai', 'Delhi', 'Pune', 'Chennai','Hyderabad', 'Kolkata', 'Ahmedabad', 'Vijayawada', 'Surat', 'Nagpur', 'Tiruppur', 'Rajkot')\n")
	desired_city = str(input())
	scrape_func(str = desired_city)

	print("\nScrape leads for another city?\n(Yes or No?)\n")
	user_resp = str(input())
	user_resp = user_resp.lower()

	if user_resp == "yes":
		main()
	else:
		print("\nCompleted... ")
		wb.save("Leads_Data.xls")

if __name__ == "__main__":
	row = 1
	print("\nScraping Indian Real Estate Project Leads (Ongoing Projects)")
	main()
