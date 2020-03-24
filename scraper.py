from bs4 import BeautifulSoup
import requests
import re

def checkUsage():
    url = 'http://10.4.21.147:3000/getusage'
    html = requests.get(url).content
    soup = BeautifulSoup(html, 'html.parser')
    table = soup.find("table")
    rows = table.find_all("tr")
    for row in rows:
        if len(row.find_all(text=re.compile('team_92'))) != 0:
            return int(row.find_all("td")[-1].text)
