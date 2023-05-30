import requests
from bs4 import BeautifulSoup
import pandas as pd
import time
import random 

series_url = 'https://www.basketball-reference.com/playoffs/2023-nba-eastern-conference-first-round-knicks-vs-cavaliers.html' # Replace 'BASE_URL' with the base URL of the website
    # Send a GET request to the series URL
series_response = requests.get(series_url)
series_soup = BeautifulSoup(series_response.content, 'html.parser')

# Find all the game summaries in the series
game_summaries = series_soup.find_all('div', class_='game_summary')
if game_summaries == None:
    print('here')

# print(game_summaries)
for game_summary in game_summaries:
        # Extract the game result details
        game_details = game_summary.find('table', class_='teams')
        game_number = game_details.find('tr', class_='date').find('td').text
        winner_team = game_details.find('tr', class_='winner').find('a').text
        loser_team = game_details.find('tr', class_='loser').find('a').text

        print(game_number)
        print(winner_team)
