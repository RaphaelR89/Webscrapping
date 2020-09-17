# Criar uma tabela de acordo com as informações do ranking dos players da NBA stats.nba.com
#Utilizar libs como requests2, pandas, beautifulsoup4 e selenium
#Aprender webscraping básico.

#Bibliotécas
import time
import requests
import pandas as pd
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from webdriver_manager.chrome import ChromeDriverManager
import json

#navegar até o site
url = "https://stats.nba.com/players/traditional/?SeasonType=Playoffs&sort=PTS&dir=-1"
top10ranking= {}

rankings = {
    '3Points': {'field': 'FG3M', 'label': '3PM'},
    'Points': {'field': 'PTS', 'label': 'PTS'},
    'Assistants': {'field': 'AST', 'label': 'AST'},
    'Rebounds': {'field': 'REB', 'label': 'REB'},
    'Steals': {'field': 'STL', 'label': 'STL'},
    'Blocks': {'field': 'BLK', 'label': 'BLK'},
}

def buildrank(type):
    driver = webdriver.Chrome(ChromeDriverManager().install())
    driver.get(url)
    #aceitar cookie
    driver.find_element_by_xpath("//*[@id='onetrust-accept-btn-handler']").click()
    #ordenar por PTS
    driver.find_element_by_xpath("//div[@class='nba-stat-table']//table//thead//tr//th[@data-field='PTS']").click()

    element = driver.find_element_by_xpath("//div[@class='nba-stat-table']//table")
    html_content = element.get_attribute('outerHTML')

    # Parsear o conteúdo com BeautifulSoup

    soup = BeautifulSoup(html_content, 'html.parser')
    table = soup.find(name='table')

    # Estruturar com o Panda

    df_full = pd.read_html(str(table))[0].head(10)
    df = df_full[["Unnamed: 0", "PLAYER", "TEAM", "PTS"]]
    df.columns = ['pos', 'player', 'team', 'total']

    # Transformar os Dados em um dicionário de dados próprio


    op10ranking['points'] = df.to_dict('records')






print(top10ranking['points'])

driver.quit()

#Converter e salvar em um arquivo JSON
js=json.dumps(top10ranking)
fp=open('ranking.json', 'w')
fp.write(js)
fp.close()
