from bs4 import BeautifulSoup as bs
from selenium import webdriver

browser = webdriver.Chrome()
url = "http://stats.nba.com/leaders/"
browser.get(url)

innerHTML = browser.execute_script("return document.body.innerHTML")
soup = bs(innerHTML, 'html.parser')

# finds all the links to a player's individual stats card 
# stores all the links in a list 
links = []
for a in soup.find_all('a', href=True):
	player_link = a['href']
	if "/player/" in player_link and "player//" not in player_link:
		links.append(player_link)
for link in links:
	print(link)

browser.quit()