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
url = "https://stats.nba.com/players/traditional/?SeasonType=Playoffs&sort=PTS&dir=-1"
driver = webdriver.Chrome(ChromeDriverManager().install())
driver.get(url)
time.sleep(3)
# ordenar por PTS
driver.find_element_by_xpath("//button[@id='onetrust-accept-btn-handler']").click()
# driver.find_element_by_xpath("/html/body/main/div[2]/div/div[2]/div/div/nba-stat-table/div[2]/div[1]/table/thead/tr/th[9]").click() clicando 2x
element = driver.find_element_by_xpath("//div[@class='nba-stat-table']//table")
html_content = element.get_attribute('outerHTML')

rankings = {
    '3Points': {'field': 'FG3M', 'label': '3PM'},
    'Points': {'field': 'PTS', 'label': 'PTS'},
    'Assistants': {'field': 'AST', 'label': 'AST'},
    'Rebounds': {'field': 'REB', 'label': 'REB'},
    'Steals': {'field': 'STL', 'label': 'STL'},
    'Blocks': {'field': 'BLK', 'label': 'BLK'},
}

# Parsear o conteúdo com BeautifulSoup
soup = BeautifulSoup(html_content, 'html.parser')
table = soup.find(name='table')

# Estruturar com o Panda
df_full = pd.read_html(str(table))[0].head(10)
df = df_full[["Unnamed: 0", "PLAYER", "TEAM", "PTS"]]
df.columns = ['pos', 'player', 'team', 'total']

# Transformar os Dados em um dicionário de dados próprio
top10ranking = {}
top10ranking['points'] = df.to_dict('records')

# Converter e salvar em um arquivo JSON
js = json.dumps(top10ranking)
fp = open('ranking.json', 'w')
fp.write(js)
fp.close()




