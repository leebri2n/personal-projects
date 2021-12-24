#Organized as [xmin, xmax, ymin, ymax]
bounds = [-100.0, 100.0, -100, 100]
grid = 30
i = 0

league_sog_x = league_s_x + league_g_x
league_sog_y = league_s_y + league_g_y
player_sog_x = player_s_x + player_g_x
player_sog_y = player_s_y + player_g_y

def normalize(list):
    for i in range(0, len(list)):
        if list[i] < 0:
            list[i] = -list[i]
    return list

#Normalized list
league_sog_x_norm = normalize(league_sog_x)
league_sog_y_norm = normalize(league_sog_y)
league_g_x_norm = normalize(league_g_x)
league_g_y_norm = normalize(league_g_y)

player_sog_x_norm = normalize(player_sog_x)
player_sog_y_norm = normalize(player_sog_y)

#league_sog_hex = plt.hexbin(league_sog_x_norm, league_sog_y_norm,
    #gridsize=grid, extent = bounds, mincnt=i)
#league_g_hex = plt.hexbin(league_g_x_norm, league_g_y_norm,
    #gridsize=grid, extent=bounds, mincnt=i)

#league_coord = league_sog_hex.get_offsets()
#print(type(league_coord))

#league_sog_freq = league_sog_hex.get_array()
#print(type(league_sog_freq))
#league_g_freq = league_g_hex.get_array()
########################################################
#fig = plt.figure(figsize=(10,10))
#ax = fig.add_subplot(1,1,1)

#ax.set_facecolor("white")
#fig.patch.set_facecolor("white")
#fig.patch.set_alpha(0.0)

#ax.set_xticklabels(labels='', alpha=0.5)
#ax.set_yticklabels(labels='', alpha=0.5)

#I = Image.open('./ice-hockey-half.png')
#ax.imshow(I)

#################################################
player = open("statovi.csv")
gret = open('statgretz.csv')
rows_o = player.read().strip().split('\n')
rows_g = gret.read().strip().split('\n')
#list of each whole row
fields_o = rows_o[0].strip().split(',')
fields_g = rows_g[0].strip().split(',')
#list of row zero, the fields
stats_o = rows_o[1:len(rows_o)]
stats_g = rows_g[1:len(rows_g)]

####################################

def list_fill(category, field_list, game_list):
    field = field_index(category, field_list)
    newlist = np.arange(0, len(stats_g), 1)

    i = 0
    for game in game_list[1:len(game_list)]:
        game_stats = game.split(',')
        entry = game_stats[field]
        newlist[i]=int(entry)
        i+=1
    j = 0
    for game in game_list[len(game_list):len(newlist)]:
        newlist[i]=0

    return newlist

def field_index(category, player_fields):
    try:
        return player_fields.index(category)
    except ValueError:
        np.nan
        print('Category not found')

game_number = list_fill('gameNumber', fields_g, stats_g)
player_goals = list_fill('goals', fields_o, stats_o)
gretz_goals = list_fill('ï»¿goaltotal', fields_g, stats_g)

j = 1
for goal in player_goals[1:len(player_goals)]:
    player_goals[j] += player_goals[j-1]
    j += 1

plt.figure(figsize=(12,8))
plt.plot(game_number, gretz_goals)
plt.plot(game_number, player_goals)
plt.show()
