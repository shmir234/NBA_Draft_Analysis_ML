# needed libraries
from urllib.request import urlopen
from bs4 import BeautifulSoup
import pandas as pd

### error checking package
import pdb
import re

### In order for this code to run as designed there needs to be a column in the dataset
# That is title Link which contains the text string needed to be entered for there
#College statistics url defined in the function. The string is formatted as
# "[First name]-[last name]-1" for a majority of players.
#I created this column using Excel and then loaded this data below

draftdf=pd.read_csv('/Users/SaadanMir/NBA/nba_draft_data.csv')

#creating a list of player links for the function to loop through
player_links=[]
for player in draftdf['Link']:
    player_links.append(player)

#Checking work
print(player_links)

#Defining a function to collect data for each player from the NBA Draft dataset
def scrape_college_statistics(links=[]):
    player_stats=[]
    #iterating through player links
    for link in links:
        try:
            player_link = link
            #replacing section in url with appropriate player_link
            url = f"https://www.sports-reference.com/cbb/players/{player_link}.html"
            html = urlopen(url)
            soup= BeautifulSoup(html, features = 'lxml')
            soup_table = soup.find(name = 'table', attrs = {'id' : 'players_per_game'})


            # get rows from table
            for row in soup_table.find_all('tr')[-1:]:# Excluding the first 'tr', since that's the table's title head
                player = {}
                player['Player']= (draftdf['Player'].loc[draftdf['Link'] == link]).item()
                player['College_Season'] = row.find('th', {'data-stat' : 'season'}).text
                player['College'] = row.find('td', {'data-stat' : 'school_name'}).text
                player['College_Games_Played'] = row.find('td', {'data-stat' : 'g'}).text
                player['College_Games_Started'] = row.find('td', {'data-stat' : 'gs'}).text
                player['College_Field_Goals_Made_Per_Game'] = row.find('td', {'data-stat' : 'fg_per_g'}).text
                player['College_Field_Goals_Attempted_Per_Game'] = row.find('td', {'data-stat' : 'fga_per_g'}).text
                player['College_FG%'] = row.find('td', {'data-stat' : 'fg_pct'}).text
                player['College_2PT_Field_Goals_Made_Per_Game'] = row.find('td', {'data-stat' : 'fg2_per_g'}).text
                player['College_2PT_Field_Goals_Attempted_Per_Game'] = row.find('td', {'data-stat' : 'fg2a_per_g'}).text
                player['College_2PT_FG%'] = row.find('td', {'data-stat' : 'fg2_pct'}).text
                player['College_3PT_Field_Goals_Made_Per_Game'] = row.find('td', {'data-stat' : 'fg3_per_g'}).text
                player['College_3PT_Field_Goals_Attempted_Per_Game'] = row.find('td', {'data-stat' : 'fg3a_per_g'}).text
                player['College_3PT_FG%'] = row.find('td', {'data-stat' : 'fg3_pct'}).text
                player['College_Free_Throws_Made_Per_Game'] = row.find('td', {'data-stat' : 'ft_per_g'}).text
                player['College_Free_Throws_Attempted_Per_Game'] = row.find('td', {'data-stat' : 'fta_per_g'}).text
                player['College_FT%'] = row.find('td', {'data-stat' : 'ft_pct'}).text
                player['Offensive_Rebounds_pergame'] = row.find('td', {'data-stat' : 'orb_per_g'}).text
                player['Defensive_Rebounds_pergame'] = row.find('td', {'data-stat' : 'drb_per_g'}).text
                player['Total_Rebounds_pergame'] = row.find('td', {'data-stat' : 'trb_per_g'}).text
                player['Assists_pergame'] = row.find('td', {'data-stat' : 'ast_per_g'}).text
                player['Steals_pergame'] = row.find('td', {'data-stat' : 'stl_per_g'}).text
                player['Blocks_pergame'] = row.find('td', {'data-stat' : 'blk_per_g'}).text
                player['Turnovers_pergame'] = row.find('td', {'data-stat' : 'tov_per_g'}).text
                player['Fouls_pergame'] = row.find('td', {'data-stat' : 'pf_per_g'}).text
                player['Points_pergame'] = row.find('td', {'data-stat' : 'pts_per_g'}).text
                player['Team_strength_of_schedule'] = row.find('td', {'data-stat' : 'sos'}).text

                player_stats.append(player)


#Adding an exception to view any errors when collecting data for each player
        except:
            print('For player: ',link, 'sys.exc_info()[0]')
#Collecting data into dataframe then placing into a csv file
    df=pd.DataFrame(player_stats)
    print(df)
    df.to_csv('College_Statistics.csv')

        ####
### Calling the function          
scrape_college_statistics(links=player_links)
