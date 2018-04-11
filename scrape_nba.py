from bs4 import BeautifulSoup as bs
from selenium import webdriver
from selenium.webdriver.support.ui import Select
from selenium.common.exceptions import NoSuchElementException, TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
import re
import pandas as pd
import requests

directory = r"/Users/anthonyniehuser/Desktop/temp-cpsc410/NBA-position-prediction/chromedriver"
url = "http://stats.nba.com/leaders/"

def main():
	browser = webdriver.Chrome()
	browser.get(url)

	# execute js scripts
	data, years = select_year(browser)
	data_with_pos = add_pos(data)
	# create a new dataframe by year 
	for i in range(len(data)):
		create_dataframe(data[i], years[i])

	# flatten our 3d list to 1d to create a dataframe containing data from all years
	total_list = []
	for i in range(len(data)):
		for j in range(len(data[i])):
			total_list.append(data[i][j])

	stat_labels = ["pos", "#","player","gp","min","pts", "fgm", "fga", "fg%", "3pm", "3pa", "3p%", "ftm", "fta", "ft%", "oreb", "dreb", "reb", "ast", "stl", "blk", "tov", "eff"]
	total_dataframe = pd.DataFrame(total_list, columns=stat_labels)
	total_dataframe.to_csv("total_dataframe", header=True, index=False)
	browser.quit()

# written by Carl Lundin
# this method takes a list of data and a string containing it's year
# method for creating dataframes seperated by what years the players played
def create_dataframe(data, years):
	# labels for each column of our dataframe
	stat_labels = ["pos", "#","player","gp","min","pts", "fgm", "fga", "fg%", "3pm", "3pa", "3p%", "ftm", "fta", "ft%", "oreb", "dreb", "reb", "ast", "stl", "blk", "tov", "eff"]
	
	df = pd.DataFrame(data, columns=stat_labels)
	path = str(years) + "_player_stats"
	df.to_csv(path, index=False, header=True)  # saves dataframe with labels

def select_year(browser):
	select = Select(WebDriverWait(browser,15).until(lambda browser: browser.find_element_by_name("Season")))
	# Data will be a 3D list that contains [year][player][stats]
	data = []
	years = []
	for option in select.options:
		years.append(option.text)
		select.select_by_visible_text(option.text)
		# append a 2D list that contains [player][stats]
		data.append(parse_page(browser))
	# returns our data list containg our stats and a list of years we extracted
	return data, years
def parse_page(browser):
	# list of players
	data = []
	select_class = "select.stats-table-pagination__select"
	try:
		# select page view to see all players at once instead of a limited amount
		select = Select(WebDriverWait(browser,2).until(lambda browser: browser.find_element_by_css_selector(select_class)))
		select.select_by_visible_text("All")
	except NoSuchElementException:
		print("limited entries (doesnt exist)")
	except TimeoutException:
		print("limited entries (timeout)")

	innerHTML = browser.execute_script("return document.body.innerHTML")
	
	# create soup and grab all the links of individual players profiles to grab their href link
	soup = bs(innerHTML, 'html.parser')
	links = add_links(soup)


	table = soup.find("table")
	tbody = table.find("tbody")
	rows = tbody.find_all("tr")
	i=0
	for tr in rows:
		columns = tr.find_all("td")
		
		# create a new list within the list of players to store a player's stats
		data.append([])
		# set the first element in the player's stats to be a string representing the link to their personal page
		# this is important because later we will take this string and replace it with the player's position
		# it must be in this position of the 3D list we are creating for the position extraction to properly work
		data[i].append(links[i])
		for td in columns:
			# append the stats of the current player
			data[i].append(td.find(text=True))
		i += 1
	# returns a 2D list in which the first element is the player and the second element is their stats
	return data

def add_links(soup):
	links = []
	for a in soup.find_all('a', href=True):
		player_link = a['href']
		if "/player/" in player_link and "player//" not in player_link:
			links.append(player_link)
	return links
main()




