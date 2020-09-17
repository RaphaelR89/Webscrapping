# Criar uma tabela de acordo com as informações do ranking dos players da NBA stats.nba.com
#Utilizar libs como requests2, pandas, beautifulsoup4 e selenium
#Aprender webscraping básico.

#Bibliotécas
import time
from pandas.io import html
import requests
import pandas as pd
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from webdriver_manager.chrome import ChromeDriverManager
import json

#navegar até o site
url = "https://stats.nba.com/players/traditional/?SeasonType=Playoffs&sort=PTS&dir=-1"
driver = webdriver.Chrome(ChromeDriverManager().install())
driver.get(url)
time.sleep(10)

driver.find_element_by_xpath("//div[@class='nba-stat-table']//table//thead//tr//th[@data-field='PTS']").click

element = driver.find_element_by_xpath("//div[@class='nba-stat-table']//table")
html_content = element.get_attribute('outerHTML')

# Parsear o conteúdo com BeautifulSoup

soup = BeautifulSoup(html_content, 'html.parser')
table = soup.find(name='table')










driver.quit()


