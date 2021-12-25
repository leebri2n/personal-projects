#Brian Lee
#@version 03.30.2021

import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
from matplotlib.pyplot import figure
import matplotlib.colors as mcolors
import matplotlib.lines as mlines

csv = open("usavacc.csv")
rows = csv.read().strip().split('\n')
columns = rows[0].strip().split(',')
csv.close()

usa_vacc = rows[1:100]
num = len(usa_vacc)

num_days = np.empty(num)
doses_available = np.empty(num)
total_vacc = np.empty(num)
total_vacc_ph = np.empty(num)
total_full = np.empty(num)
daily_vacc = np.empty(num)
daily_vacc_pm = np.empty(num)
available_vacc = np.empty(num)

def get_index(category):
    try:
        return columns.index(category, 0, len(columns))
    except ValueError:
        return np.nan

def fill_list(category, list):
    index = 0
    cat_index = get_index(category)

    for day in usa_vacc:
        day_info = day.split(',')
        day_stat = day_info[cat_index]

        if day_stat == '':
            list[index] = 0
        else:
            list[index] = float(day_stat)
        index += 1

    return list

def list_average(list):
    sum = list[0]
    index = 1
    newlist = np.empty(num)
    for entry in list[1:len(list)]:
        sum += list[index]
        newlist[index] = float(sum/index)
        index += 1

    return newlist

fill_list('day_num', num_days)
fill_list('people_vaccinated', total_vacc)
fill_list('people_vaccinated_per_hundred', total_vacc_ph)
fill_list('daily_vaccinations', daily_vacc)
fill_list('daily_vaccinations_per_million', daily_vacc_pm)
fill_list('people_fully_vaccinated', total_full)
fill_list('total_vaccinations', available_vacc)

#totals of part and full
plt.figure(figsize=(12,6))
plt.plot(num_days, total_vacc, color='springgreen')
plt.plot(num_days, total_full, color='violet')
plt.title('United States COVID-19 Vaccination Effort in 100 Days, Gross Totals')
plt.xlabel('Day Number')
plt.ylabel('Number of People (in 10mil)')
part_line = mlines.Line2D([],[],color='springgreen',
    label='Total Persons Given at Least One Dose')
full_line = mlines.Line2D([],[],color='violet',
    label='Total Persons Fully Vaccinated')
plt.legend(handles=[part_line, full_line])

#daily and daily moving average
moving_average = list_average(daily_vacc)
plt.figure(figsize=(12,6))
plt.plot(num_days, daily_vacc, color='dodgerblue')
plt.plot(num_days, moving_average, color='rebeccapurple')
plt.title('United States COVID-19 Vaccination Effort in 100 Days, Daily Vaccinations')
plt.xlabel('Day Number')
plt.ylabel('Number of People (Millions)')
daily_line = mlines.Line2D([],[],color='dodgerblue',
    label='Daily Number of Vaccinations')
av_line = mlines.Line2D([],[],color='rebeccapurple',
    label='Average Daily Number of Vaccinations')
plt.legend(handles=[daily_line, av_line])

#total vs doses available
plt.figure(figsize=(12,6))
plt.plot(num_days, total_vacc, color='springgreen')
plt.plot(num_days, available_vacc, color='indianred')
plt.title('United States COVID-19 Vaccination Effort, Available Doses and Total Vaccination')
plt.xlabel('Day Number')
plt.ylabel('Number of People (by 100 Million)')
total_line = mlines.Line2D([],[],color='springgreen',
    label='Total Persons Given at Least One Dose')
avail_line = mlines.Line2D([],[],color='indianred',
    label='Available Doses')
plt.legend(handles=[total_line, avail_line])

plt.show()
