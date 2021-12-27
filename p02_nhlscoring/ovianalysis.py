#Brian Lee
#Version @8.20.21
#Working version @12.20.2021

#Load packages
import requests as req
import json
import numpy as np
import math
from hockey_rink import NHLRink
import matplotlib.pyplot as plt
from matplotlib.pyplot import figure
import pandas as pd
from PIL import Image
import matplotlib.lines as mlines
from matplotlib.patches import RegularPolygon
from PIL import Image
from matplotlib.colors import ListedColormap
from matplotlib.colors import LinearSegmentedColormap
import matplotlib.colors as mcolors

#########################################################
#Initialize dictionary, variables
games18 = 82 #82 games per season
id = 8471214 #Alex Ovechkin NHLID

leaguewide_stats = {}
leaguewide_stats['Shot'] = {}
leaguewide_stats['Shot']['x'] = []
leaguewide_stats['Shot']['y'] = []
leaguewide_stats['Shot']['time'] = []
leaguewide_stats['Goal'] = {}
leaguewide_stats['Goal']['x'] = []
leaguewide_stats['Goal']['y'] = []
leaguewide_stats['Goal']['time'] = []

player_stats = {}
player_stats['Shot'] = {}
player_stats['Shot']['x'] = []
player_stats['Shot']['y'] = []
player_stats['Shot']['time'] = []
player_stats['Goal'] = {}
player_stats['Goal']['x'] = []
player_stats['Goal']['y'] = []
player_stats['Goal']['time'] = []

#Master function of sorts that stores every play of every game for a player
# in a given year.
def store_year(year, until, searchid):
    end_year = int(year) + 1
    print("Appending data for year " + year + "-" + str(end_year)+ "...")

    for i in range(1, until):
        with open('./'+year+'Data'+'/'+
            year+'_g'+str(i)+'Capitals.json') as file:
            game = json.load(file)
            all_plays = game['liveData']['plays']['allPlays']
            fill_dict(all_plays, searchid)

#Fills the dictionary with all the right plays
def fill_dict(all_plays, searchid):
    for play in all_plays:
        if 'players' in play:
            j = 0

            #Differentiates if a the desired player is part of the play.
            player_list = play['players']
            for player in player_list:
                matchid = player_list[0]['player']['id']
                if searchid == matchid:
                    player_dict = player_stats
                    sort_event(play, player_dict)
                else:
                    player_dict = leaguewide_stats
                    sort_event(play, player_dict)
                j += 1

#Categorizes events based on type, i.e, shot, goal, etc.
def sort_event(play, dict):
    #Initialize for compactness purposes
    xs = dict['Shot']['x']
    ys = dict['Shot']['y']
    ts = dict['Shot']['time']
    xg = dict['Goal']['x']
    yg = dict['Goal']['y']
    tg = dict['Goal']['time']

    event = play["result"]['event'] #The name of type of event
    coordinates = play['coordinates'] #Necessary for special cases of
    #bad data where only one coordinate exists for the event

    if len(coordinates) == 2:
        if event == "Shot":
            xcoord = play['coordinates']['x']
            ycoord = play['coordinates']['y']
            time = play['about']['periodTime']
            xs.append(xcoord)
            ys.append(ycoord)
            ts.append(time)
        elif event == "Goal":
            xcoord = play['coordinates']['x']
            ycoord = play['coordinates']['y']
            time = play['about']['periodTime']
            xg.append(xcoord)
            yg.append(ycoord)
            tg.append(time)


#store_year('2010', 82, id)
#store_year('2011', 82, id)
#store_year('2012', 48, id)
#store_year('2013', 82, id)

store_year('2018', 82, id)
store_year('2019', 82, id)
store_year('2020', 56, id)

print("~~~~~~~~~~~~~~~~~~")

#################################################
#Initialize dataframes to use pandas data analysis
player_df = pd.DataFrame(player_stats)
league_df = pd.DataFrame(leaguewide_stats)

league_sog_x = league_df['Shot']['x'] + league_df['Goal']['x']
league_sog_y = league_df['Shot']['y'] + league_df['Goal']['y']
player_sog_x = player_df['Shot']['x'] + player_df['Goal']['x']
player_sog_y = player_df['Shot']['y'] + player_df['Goal']['y']

#Assumed that goals are added to where shots end. Create list to classify events.
def goalcheck(type_df):
    test = list()
    for i in range(len(type_df['Shot']['x'])):
        test.append(0)
    for i in range(len(type_df['Shot']['x']),
            len(type_df['Shot']['x'] + type_df['Goal']['x'])):
        test.append(1)
    return test
league_goalcheck = goalcheck(league_df)
player_goalcheck = goalcheck(player_df)
league_goalcheck = np.array(league_goalcheck)
player_goalcheck = np.array(player_goalcheck)

#Make new dataframes with a check if the shot is a goal or not
#League
league_sog_x = np.array(league_sog_x)
np.abs(league_sog_x, out=league_sog_x) #Normalize coordinates
league_sog_y = np.array(league_sog_y) #No normalization needed for y
league_g_x = np.abs(np.array(league_df['Goal']['x']))
league_g_y = np.array(league_df['Goal']['y'])

league_sog_df = pd.DataFrame()
league_sog_df['x'] = league_sog_x
league_sog_df['y'] = league_sog_y
league_sog_df['goalcheck'] = league_goalcheck

#Player
player_sog_x = np.array(player_sog_x)
np.abs(player_sog_x, out=player_sog_x)
player_sog_y = np.array(player_sog_y)
player_g_x = np.abs(np.array(player_df['Goal']['x']))
player_g_y = np.array(player_df['Goal']['y'])

player_sog_df = pd.DataFrame()
player_sog_df['x'] = player_sog_x
player_sog_df['y'] = player_sog_y
player_sog_df['goalcheck'] = player_goalcheck

#######################################################
#First figure, for preliminary visualization
fig, ax = plt.subplots(1, 2, figsize=(15, 8))
rink = NHLRink(rotation=90)
for i in range(2):
    rink.draw(ax=ax[i], display_range="ozone")

#Visualize raw shot-goal patterns
#rink.heatmap(league_sog_df.x, league_sog_df.y,
    #values=league_sog_df.goalcheck, cmap="magma", ax=ax[0], binsize=2)
#rink.heatmap(player_sog_df.x, player_sog_df.y,
    #values=player_sog_df.goalcheck, cmap="magma", ax=ax[1], binsize=2)

rink.contourf(league_sog_df.x, league_sog_df.y,
    values=league_sog_df.goalcheck, ax=ax[0], binsize=20, cmap="bwr", levels=100)
rink.contourf(player_sog_df.x, player_sog_df.y,
    values=player_sog_df.goalcheck, ax=ax[1], binsize=20, cmap="bwr", levels=100)

################################################
#Visualize relative efficiencies
bounds = [-100.0, 100.0, -100, 100]
grid = 30
cnt = 0
color_map = plt.cm.winter
positive_cm = ListedColormap([mcolors.ColorConverter().to_rgb('#e1e5e5'),
    mcolors.ColorConverter().to_rgb('#d63b36')])
negative_cm = ListedColormap([mcolors.ColorConverter().to_rgb('#e1e5e5'),
    mcolors.ColorConverter().to_rgb('#28aee4')])

width = 50
height= 50
scalex = width/100*1.25
scaley = height/100*1.8
scalehex = 4.4*scalex

###########################################################
league_sog_hex = plt.hexbin(league_sog_x, league_sog_y,
    gridsize=grid, extent=bounds, mincnt=cnt, alpha=0)
league_g_hex = plt.hexbin(league_g_x, league_g_y,
    gridsize=grid, extent=bounds, mincnt=cnt, alpha=0)

league_offsets = league_sog_hex.get_offsets()
league_sog_freq = league_sog_hex.get_array()
league_g_freq = league_g_hex.get_array()

fig2 = plt.figure(figsize=(8,8))
ax2 = fig2.add_subplot(111)
relrink = NHLRink()
rinkdraw = relrink.draw(display_range="ozone")

for i,j in enumerate(league_offsets):
    if league_sog_freq[i] < 25: continue
    league_sog_scale = league_sog_freq[i]/max(league_sog_freq)
    radius = scalehex * math.sqrt(league_sog_scale)

    hex = RegularPolygon((28+j[0]*scalex, (height/2)-j[1]*scaley-25), numVertices=6,
        radius=radius, orientation=np.radians(0), alpha=0.5)
    rinkdraw.add_patch(hex)

#########################################################
fig3 = plt.figure(figsize=(8,8))
ax3 = fig3.add_subplot(111)
rinkdraw2 = relrink.draw(display_range="ozone")

player_sog_hex = plt.hexbin(player_sog_x, player_sog_y,
    gridsize=grid, extent=bounds, mincnt=cnt, alpha=0)
player_g_hex = plt.hexbin(player_g_x, player_g_y,
    gridsize=grid, extent=bounds, mincnt=cnt, alpha=0)

player_offsets = player_sog_hex.get_offsets()
player_sog_freq = player_sog_hex.get_array()

player_g_offsets = player_g_hex.get_offsets()
player_g_freq = player_g_hex.get_array()

#Visualize where player takes shots
for i,j in enumerate(player_offsets):
    if player_sog_freq[i] < 20: continue
    player_sog_scale = player_sog_freq[i]/max(player_sog_freq)
    radius = scalehex * math.sqrt(player_sog_scale)

    hex = RegularPolygon((28+j[0]*scalex, (height/2)-j[1]*scaley-25), numVertices=6,
        radius=radius, orientation=np.radians(0), alpha=0.5)
    rinkdraw2.add_patch(hex)

#Visualize where player scores
for i, j in enumerate(player_g_offsets):
    if player_g_freq[i] < 5: continue
    player_g_scale = player_g_freq[i]/max(player_g_freq)
    radius2 = scalehex * math.sqrt(player_g_scale)

    hex2 = RegularPolygon((28+j[0]*scalex, (height/2)-j[1]*scaley-25), numVertices=6,
        radius=radius2, orientation=np.radians(0), alpha=1.0, facecolor="aquamarine")
    rinkdraw2.add_patch(hex2)
###############################################
league_eff = list()
player_eff = list()
comp_eff = list()

for i in range(0, len(league_sog_freq)):
    if league_sog_freq[i] < 5 or player_sog_freq[i] < 5: continue
    league_eff_local = league_g_freq[i]/league_sog_freq[i]
    player_eff_local = player_g_freq[i]/player_sog_freq[i]

    league_eff.append(league_eff_local)
    player_eff.append(player_eff_local)
    comp_eff.append(player_eff_local-league_eff_local)

for i, j in enumerate(player_offsets):
    if player_sog_freq[i] < 5: continue

    player_sog_scale = player_sog_freq[i]/max(player_sog_freq)
    radius3 = scalehex * math.sqrt(player_sog_scale)

    league_eff_local = league_g_freq[i]/league_sog_freq[i]
    player_eff_local = player_g_freq[i]/player_sog_freq[i]

    comp_eff_local = player_eff_local-league_eff_local

    if comp_eff_local > 0:
        colour = positive_cm(math.pow(comp_eff_local, 0.2))
    else:
        colour = negative_cm(math.pow(-comp_eff_local, 0.5))

    hex3 = RegularPolygon((28+j[0]*scalex, (height/2)-j[1]*scaley-25), numVertices=6,
        radius=radius3, orientation=np.radians(0), alpha=1.0, facecolor=colour)

    rinkdraw2.add_patch(hex3)

###############################################
plt.show()
