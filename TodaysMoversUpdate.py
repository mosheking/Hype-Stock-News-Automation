from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.chrome.service import Service
import pandas as pd
from time import sleep

from selenium.webdriver.common.keys import Keys

import numpy as np



import requests

#header for https requests
header = {
  "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.75 Safari/537.36",
  "X-Requested-With": "XMLHttpRequest"
}


website = "https://www.investing.com/equities/top-stock-gainers"
path = "/Users/mosheshtaygrud/Desktop/CodingProjects/Selenium/chromedriver"


# service = Service(executable_path=path)

driver = webdriver.Chrome(executable_path=path)

r = requests.get(website, headers=header)
scraper = pd.read_html(r.text)[0]

scraper = scraper.iloc[ 0:25 , [1,2,3,4,5,6,7,8]]

companyNames = scraper['Name'].values

percentChange = scraper['Chg. %'].values


companyArticles = []
    

#l0op over companies and get their news links
for i in companyNames:
    driver.get('https://www.google.com/')
    driver.find_element_by_xpath('/html/body/div[1]/div[3]/form/div[1]/div[1]/div[1]/div/div[2]/input').send_keys(i + ' stock news' + Keys.ENTER)
    driver.find_element_by_xpath('//*[@id="hdtb-msb"]/div[1]/div/div[2]/a').click()
    
    firstHalfOfXpath = '//*[@id="rso"]/div/div/div['
    secondHalfOfXpath = ']/div/div/a'
    #get the first 6 articles in the news section
    articles = {
        1: '',
        2: '',
        3: '',
        4: '',
        5: '',  
        6: ''
    } 
    for i in range(6): 
        try:
            articles[i + 1] = str(driver.find_element_by_xpath(firstHalfOfXpath + str(i+1) + secondHalfOfXpath).get_attribute('href'))
        except NoSuchElementException:
            continue
    companyArticles.append(articles)
    
    #lnks = driver.find_elements_by_tag_name("a")
    sleep(4)

message = ''

counter = 1

for company in companyNames:
    #add 
    message +=  'Company #' + str(counter) + '  ' +  company  + ' SOARED ' + percentChange[counter - 1] + "\n read following articles: \n" 
    for i in range(6): 
        if 'investorsobserver' in companyArticles[counter - 1][i+1]:
            continue
        message += companyArticles[counter - 1][i + 1] + "\n"
    counter+=1

       

# =============================================================================
# Sending a message to myself with textbelt api
# =============================================================================
# =============================================================================
# resp = requests.post('https://textbelt.com/text', {
#   'phone': '8455129834',
#   'message': message,
#   'key': 'textbelt'
#  })
# print(resp.json())
# =============================================================================




