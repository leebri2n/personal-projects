#Brian Lee
#@version1 08.03.2021

import requests as req
import json
import csv

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.pyplot import figure
import pandas as pd
import matplotlib.colors as mcolors
import matplotlib.lines as mlines

max_games = 1271

def games_write(year, games, teamid):
    selected_games = games_search(year, games, teamid)

    print('Saving game files...')
    for j in range(0, len(selected_games)):
        game_data = selected_games[j]
        with open('./' + year + 'Data/' + year +
            '_g' + str(j+1) + 'Capitals.json', 'w') as file:
            json.dump(game_data, file)

        dec = (j / len(selected_games)) * 100
        perc = "{:.2f}".format(dec)
        print(str(perc) + ' %')

    print("COMPLETED.")

def games_search(year, games, teamid):
    team_games = []

    print("Searching for Capitals games, year:" + str(year))
    for i in range(1, games):
        raw = req.get(url='http://statsapi.web.nhl.com/api/v1/game/' +
            year + '02' + str(i).zfill(4) + '/feed/live')
        data = raw.json() #dictionary #one game

        away = data["gameData"]["teams"]["away"]["id"]
        home = data["gameData"]["teams"]["home"]["id"]

        if (away == teamid) or (home == teamid):
            team_games.append(data)

        dec = (i / games) * 100
        perc = "{:.2f}".format(dec)
        print(str(perc) + ' %')

    print("COMPLETED.")
    return(team_games)

#games_write('2005', 1230, 15)
#games_write('2006', 1230, 15)
#games_write('2007', 1230, 15)
#games_write('2008', 1230, 15)
#games_write('2009', 1230, 15)
#games_write('2010', 1230, 15)
#games_write('2011', 1230, 15)
games_write('2012', 720, 15)
games_write('2013', 1230, 15)
games_write('2014', 1230, 15)
games_write('2015', 1230, 15)
games_write('2016', 1230, 15)
#games_write('2018', max_games, 15)
#games_write('2017', max_games, 15)
#games_write('2019', max_games, 15)
#games_write('2020', 868, 15)




################################################
