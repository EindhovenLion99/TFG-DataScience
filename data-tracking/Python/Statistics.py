import sys
import pandas as pd
import matplotlib.pyplot as plt
import math


def plotTeamPosesion(events):
  teams = ["Away", "Home"]
  total_passes = events.loc[events['Type'] == 'PASS', 'Type'].count()
  home_possession = events.loc[(events['Type'] == 'PASS') & (events['Team'] == 'Home'), 'Type'].count() / total_passes
  away_possession = events.loc[(events['Type'] == 'PASS') & (events['Team'] == 'Away'), 'Type'].count() / total_passes
  possession = [home_possession * 100, away_possession * 100]

  data = {'Team': teams, 'Possession': possession}
  df = pd.DataFrame(data ,columns=['Team','Possession'])
  df = df.set_index('Team')
  df.plot(kind='pie', y="Possession")

# Crea un grafico del total de eventos de cada equipo

def plotTeamStats(events, type, subtype=None):
  label = ""
  if subtype:
    if type.upper() in events['Type'].unique() and subtype.upper() in events.loc[events['Type'] == type.upper(), 'Subtype'].unique():
        print("Entra 1")
        stats = events.loc[(events['Type'] == type.upper()) & (events['Subtype'] == subtype.upper())]
        team_stats = stats.groupby('Team')['Type'].count()
        label = type.upper() + " - " + subtype.upper()
    else:
      print("TYPES NOT AVAILABLE")
      sys.exit()
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
  print(team_stats)
  team_stats.plot(kind = 'bar', ylabel = label, yticks = range(0,max_stat+1,math.ceil(max_stat/10)), color=['blue', 'red',])

