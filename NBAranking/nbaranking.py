# Criar uma tabela de acordo com as informações do ranking dos players da NBA stats.nba.com
# Utilizar libs como requests2, pandas, beautifulsoup4 e selenium
# Aprender webscraping básico.

# Bibliotécas
import time
import requests
import pandas as pd
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from webdriver_manager.chrome import ChromeDriverManager
from selenium.common.exceptions import NoSuchElementException    
import json

# navegar até o site
url = "https://stats.nba.com/players/traditional/?SeasonType=Playoffs&sort=PLAYER_NAME&dir=1"
driver = webdriver.Chrome(ChromeDriverManager().install())
driver.get(url)
time.sleep(3)

#POPUP do site
popup = driver.find_element_by_xpath("//button[@id='onetrust-accept-btn-handler']")
if popup:
    popup.click()
# ordenar por categorias
top10ranking = {}
rankings = {
    '3points': {'field': 'FG3M', 'label': '3PM'},
    'points': {'field': 'PTS', 'label': 'PTS'},
    'assistants': {'field': 'AST', 'label': 'AST'},
    'rebounds': {'field': 'REB', 'label': 'REB'},
    'steals': {'field': 'STL', 'label': 'STL'},
    'blocks': {'field': 'BLK', 'label': 'BLK'},
}

#Função da tabela
def buildrank(type):
    field = rankings[type]['field']
    label = rankings[type]['label']
    
    driver.find_element_by_xpath(f"//div[@class='nba-stat-table']//table//thead//tr//th[@data-field='{field}']").click()
    element = driver.find_element_by_xpath("//div[@class='nba-stat-table']//table")
    html_content = element.get_attribute('outerHTML')
    # Parsear o conteúdo com BeautifulSoup
    soup = BeautifulSoup(html_content, 'html.parser')
    table = soup.find(name='table')
    # Estruturar com o Panda
    df_full = pd.read_html(str(table))[0].head(10)
    df = df_full[["Unnamed: 0", "PLAYER", "TEAM", label]]
    df.columns = ['pos', 'player', 'team', 'total']
    # Transformar os Dados em um dicionário de dados próprio
    return df.to_dict('records')

top10ranking['points'] = buildrank('points')

for i in rankings:
    top10ranking[i] = buildrank(i)

#Fechar bot
driver.quit()

# Converter e salvar em um arquivo JSON
js = json.dumps(top10ranking)
fp = open('ranking.json', 'w')
fp.write(js)
fp.close()