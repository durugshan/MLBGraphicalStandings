# -*- coding: utf-8 -*-
"""
Created on Sun Jul 15 13:16:01 2018

@author: Durugshan
"""

from urllib.request import urlopen
from bs4 import BeautifulSoup
import pandas as pd
import numpy as np
import time

def scrapeStandings(index):

    teamName = teams_cols[index]
    # specific url that we need
    standings_source = 'https://www.baseball-reference.com/teams/'+ teamName + '/2018-schedule-scores.shtml'
    
    # opening the url
    page = urlopen(standings_source)
    
    # loading it into BS
    soup = BeautifulSoup(page)
    
    #name_box = soup.find('table', attrs={'class': 'overthrow table_container'})
    #
    #table = soup.find_all('table')
    
    # get column headers by first column
    column_headers = [th.getText() for th in 
                      soup.find('tr').findAll('th')]
    
    # skip the first 2 header rows
    data_rows = soup.findAll('tr')[1:] 
    
    player_data = [[td.getText() for td in data_rows[i].findAll('td')]
                for i in range(len(data_rows))]
    
    player_data_02 = []  # create an empty list to hold all the data
    
    for i in range(len(data_rows)):  # for each table row
        player_row = []  # create an empty list for each pick/player
    
        # for each table data element from each table row
        for td in data_rows[i].findAll('td'):        
            # get the text content and append to the player_row 
            player_row.append(td.getText())        
    
        # then append each pick/player to the player_data matrix
        player_data_02.append(player_row)
        
    df = pd.DataFrame(player_data, columns=column_headers[1:])
    df2 = df[df['Date'].notnull()]
    df2 = df2.reset_index(drop=True)
    
    return df2

def fillStandings(df2, index):
    ml_standings.loc[0][teams_cols[index]] = 0
    for i in range(len(df2)):
        
        if type(df2.loc[i]['W-L']) == str:
            currentWL = int(df2.loc[i]['W-L'].split('-')[0]) - int(df2.loc[i]['W-L'].split('-')[1])
            print(currentWL)
            ml_standings.loc[i+1][teams_cols[index]] = currentWL 
        else:
            continue

teams_cols = ['GM#', 'BOS', 'NYY', 'BAL', 'TBR', 'TOR', 'CHW', 'CLE', 'DET', 'KCR', 'MIN', \
              'HOU', 'LAA', 'OAK', 'SEA', 'TEX', 'ATL', 'MIA', 'NYM', 'PHI', 'WSN', \
              'CHC', 'CIN', 'MIL', 'PIT', 'STL', 'ARI', 'COL',\
              'LAD', 'SDP','SFG']

ml_standings = pd.DataFrame(index = np.arange(0,163),columns = teams_cols)

for i in range(len(ml_standings)):
    ml_standings.loc[i]['GM#'] = i

for index in range(1, len(teams_cols)):                  
    tempdf = scrapeStandings(index)
    fillStandings(tempdf, index)
                
timestr = time.strftime("%Y%m%d-%H%M")
ml_standings.to_csv('UpdatedStandings - ' + timestr +'.csv')     
  