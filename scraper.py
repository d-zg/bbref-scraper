import requests
from bs4 import BeautifulSoup
import pandas as pd
import time
import random 
# URL to scrape
url = 'https://www.basketball-reference.com/playoffs/series.html'

# Get the HTML content
response = requests.get(url)
html_content = response.content

print(response.status_code)

# Print the headers
for h,v in response.headers.items():
    print(h, ':', v)

# Parse the HTML content
soup = BeautifulSoup(html_content, 'html.parser')

# Find all the rows in the main table
rows = soup.find_all('tr')

desired_rows = []

for row in rows:
    if row.find('td', {'data-stat': 'winner'}) is not None:
        desired_rows.append(row)


# make a pandas dataframe
df = pd.DataFrame(columns=['Series', 'Winner', 'This Team', 'Record', 'Win Order'])


for row in desired_rows: 
    # Extract the winner of the series
    time.sleep(random.randint(1,3))
    winner = row.find('td', {'data-stat': 'winner'}).find('a').text

    # Extract the link to the series details
    series_link = row.find('td', {'data-stat': 'series'}).find('a')['href']
    series_url = 'https://www.basketball-reference.com' + series_link  # Replace 'BASE_URL' with the base URL of the website
        # Send a GET request to the series URL
    series_response = requests.get(series_url)
    series_soup = BeautifulSoup(series_response.content, 'html.parser')
    
    # Find all the game summaries in the series
    game_summaries = series_soup.find_all('div', class_='game_summary')
    winner_losses, winner_wins, = 0, 0
    winner_order = ""
    loser_losses, loser_wins = 0, 0
    loser_order = ""

    for game_summary in game_summaries:
        # Extract the game result details
        game_details = game_summary.find('table', class_='teams')
        game_number = game_details.find('tr', class_='date').find('td').text
        winner_team = game_details.find('tr', class_='winner').find('a').text
        loser_team = game_details.find('tr', class_='loser').find('a').text
        
        if winner_team == winner:
            winner_wins += 1
            winner_order += "W"
            loser_order += "L"
            loser_losses += 1
        else:
            winner_losses += 1
            winner_order += "L"
            loser_order += "W"
            loser_wins += 1
        
        # add two rows to the dataframe, one for the winner and one for the loser
        df = df._append({'Series': series_url, 'Winner': winner, 'This Team': winner_team, 'Record': str(winner_wins) + '-' + str(winner_losses), 'Win Order': winner_order}, ignore_index=True)
        df = df._append({'Series': series_url, 'Winner': winner, 'This Team': loser_team, 'Record': str(loser_wins) + '-' + str(loser_losses), 'Win Order': loser_order}, ignore_index=True)
        # Extract and print the desired stats from the table
    print(winner)
df.to_csv('nba_playoff_results.csv', index=False)