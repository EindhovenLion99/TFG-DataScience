import sys
import pandas as pd
import matplotlib.pyplot as plt
import math


def plotTeamPosesion(events, figsize=(10,10)):
  teams = ["Away", "Home"]
  total_passes = events.loc[events['Type'] == 'PASS', 'Type'].count()
  home_possession = events.loc[(events['Type'] == 'PASS') & (events['Team'] == 'Home'), 'Type'].count() / total_passes
  away_possession = events.loc[(events['Type'] == 'PASS') & (events['Team'] == 'Away'), 'Type'].count() / total_passes
  possession = [home_possession * 100, away_possession * 100]

  data = {'Team': teams, 'Possession': possession}
  df = pd.DataFrame(data ,columns=['Team','Possession'])
  df = df.set_index('Team')
  df.plot(kind='pie', y="Possession", shadow=True, startangle=90, autopct='%1.1f%%', figsize=figsize, colors=['blue','red'])

# Crea un grafico del total de eventos de cada equipo

def plotTeamStats(events, type, subtype=None):
  label = ""
  if subtype:
    stats = events.loc[(events['Type'] == type.upper()) & (events['Subtype'].str.contains(subtype.upper()))]
    team_stats = stats.groupby('Team')['Type'].count()
    label = type.upper() + " - " + subtype.upper()
  elif type.upper() in events['Type'].unique():
    stats = events.loc[events['Type'] == type.upper()]
    team_stats = stats.groupby('Team')['Type'].count()
  elif type.upper() in events['Subtype'].unique():
    stats = events.loc[events['Subtype'] == type.upper()]
    team_stats = stats.groupby('Team')['Subtype'].count()
  else:
    print("NO COLUMN DETECTED")
    sys.exit()
  max_stat = team_stats.max()
  if label == "":
    label = type.upper()
  ax = team_stats.plot(kind = 'bar', ylabel = label, yticks = range(0,max_stat+1,math.ceil(max_stat/10)), color=['blue', 'red',])
  for container in ax.containers:
    ax.bar_label(container)
