from bs4 import BeautifulSoup
import requests

html_text = requests.get("https://www.pro-football-reference.com/years/2022/games.htm").text
soup = BeautifulSoup(html_text, 'lxml')

print(source)