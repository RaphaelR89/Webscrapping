import requests
import pandas as pd
from bs4 import BeautifulSoup
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
import json

# Grab content from URL (Pegar conteúdo HTML a partir da URL)
url = "https://stats.nba.com/players/traditional/?SeasonType=Playoffs&sort=PTS&dir=-1"
top10ranking = {}

rankings = {
    '3points': {'field': 'FG3M', 'label': '3PM'},
    'points': {'field': 'PTS', 'label': 'PTS'},
    'assistants': {'field': 'AST', 'label': 'AST'},
    'rebounds': {'field': 'REB', 'label': 'REB'},
    'steals': {'field': 'STL', 'label': 'STL'},
    'blocks': {'field': 'BLK', 'label': 'BLK'},
}


def buildrank(type):

    # field = rankings[type]['field']
    # label = rankings[type]['label']

    driver.find_element_by_xpath("//div[@class='nba-stat-table']//table//thead//tr//th[@data-field='PTS']").click()

    element = driver.find_element_by_xpath(
        "//div[@class='nba-stat-table']//table")
    html_content = element.get_attribute('outerHTML')

    # Parse HTML (Parsear o conteúdo HTML) - BeaultifulSoup
    soup = BeautifulSoup(html_content, 'html.parser')
    table = soup.find(name='table')

    # Data Structure Conversion (Estruturar conteúdo em um Data Frame) - Pandas
    df_full = pd.read_html(str(table))[0].head(10)
    df = df_full[['Unnamed: 0', 'PLAYER', 'TEAM', 'PTS']]
    df.columns = ['pos', 'player', 'team', 'total']

    # Convert to Dict (Transformar os Dados em um Dicionário de dados próprio)
    return df.to_dict('records')




driver = webdriver.Chrome(ChromeDriverManager().install())

driver.get(url)
driver.implicitly_wait(10)  # in seconds

for k in rankings:
    top10ranking[k] = buildrank(k)

driver.quit()

# Dump and Save to JSON file (Converter e salvar em um arquivo JSON)
with open('ranking2.json', 'w', encoding='utf-8') as jp:
    js = json.dumps(top10ranking, indent=4)
    jp.write(js)