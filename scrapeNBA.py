from bs4 import BeautifulSoup as bs
from selenium import webdriver
from selenium.webdriver.support.ui import Select
from selenium.common.exceptions import NoSuchElementException, TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
import json
import re

directory = r"/Users/anthonyniehuser/Desktop/temp-cpsc410/NBA-position-prediction/chromedriver"
url = "http://stats.nba.com/leaders/"

def main():
	
	

	browser = webdriver.Chrome(directory)
	browser.get(url)

	# execute js scripts
	
	# get soyup object of dynamically loaded html

	data = select_year(browser)

	with open("nba-stats.json", "w+") as outfile:
		json.dump(data, outfile)
	

	# close browser
	browser.quit()

def to_json(data):
	stat_labels = ["#","player","gp","min","pts", "fgm", "fga", "fg%", "3pm", "3pa", "3p%", "ftm", "fta", "ft%", "oreb", "dreb", "reb", "ast", "stl", "blk", "tov", "eff"]
	players = {}
	

	for j in range(0,len(data)):
		stats = {}
		for i in range(2,len(stat_labels)):
			stats[stat_labels[i]] = data[j][i]
		players[data[j][1]] = stats
	
	return players

def select_year(browser):
	js = {}
	select = Select(WebDriverWait(browser,15).until(lambda browser: browser.find_element_by_name("Season")))
	for option in select.options:
		
		select.select_by_visible_text(option.text)
		# browser.implicitly_wait(1)
		data = parse_page(browser)
		js[option.text] = to_json(data)
		browser.get(url)
	return js

def parse_page(browser):
	data = []
	select_class = "select.stats-table-pagination__select"
	try:
		select = Select(WebDriverWait(browser,2).until(lambda browser: browser.find_element_by_css_selector(select_class)))
		select.select_by_visible_text("All")
	except NoSuchElementException:
		print("limited entries (doesnt exist)")
	except TimeoutException:
		print("limited entries (timeout)")

	innerHTML = browser.execute_script("return document.body.innerHTML")
	

	soup = bs(innerHTML, 'html.parser')

	links = add_links(soup)

	table = soup.find("table")
	tbody = table.find("tbody")
	rows = tbody.find_all("tr")
	i=0
	for tr in rows:
		columns = tr.find_all("td")
		
		data.append([])
		for td in columns:
			data[i].append(td.find(text=True))
		if i==0:
			data[i].append(position_scrape(browser=browser, link=links[i]))
		print(data[i])
		i += 1
	return data

def add_links(soup):
	links = []
	table = soup.find("table")
	for a in table.find_all("a", href=re.compile("/player/")):
		# print(a)
		# player_link = a['href']
		# if "/player/" in player_link and "player//" not in player_link:
		links.append(a)
	return links

def position_scrape(browser, link):
	beginning = "https://stats.nba.com"
	# player_url = beginning + link
	action = ActionChains(browser)
	action.move_to_element(link).key_down(Keys.SHIFT).click(link).key_up(Keys.SHIFT).perform()
	# link.send_keys(Keys.COMMAND + Keys.RETURN)
	# browser.get(player_url)

	# execute js scripts
	# innerHTML = browser.execute_script("return document.body.innerHTML")

	# find elements with player position
	# elements = browser.find_elements_by_class_name("player-summary__player-pos")
	
	# close browser
	# browser.find_element_by_tag_name("body").send_keys(Keys.COMMAND + 'w')

	# return elements[0].text

	

main()




