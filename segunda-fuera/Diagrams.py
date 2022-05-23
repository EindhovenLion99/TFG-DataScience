# %%
from Clases.team import team
from getTeamsWithCity import getTeamsWithCity
import csv
import matplotlib.pyplot as plt
from matplotlib.pyplot import figure
import pandas as pd

# %%
teams = getTeamsWithCity('CSV/teams.csv')
teams_total = []
for team in teams:
  with open('CSV/TeamsDistance.csv') as csv_file:
    csv_reader = csv.reader(csv_file, delimiter=',')
    line_count = 0
    team_name = ""
    total_team_distance = 0
    for row in csv_reader:
      if line_count == 0:
        line_count += 1
      else:
        if row[0] == team.name or row[3] == team.name:
          total_team_distance += float(row[6])

    teams_total.append({
      "name": team.name,
      "total_dist": round(total_team_distance, 2)
    })

# %%

eje_X = []
eje_Y = []
for team in teams_total:
  eje_X.append(team["name"])
  eje_Y.append(team["total_dist"])

data = {'Equipo': eje_X, 'Distancia': eje_Y}

df = pd.DataFrame(data, columns=['Equipo', 'Distancia'])

df.sort_values(by=['Distancia'], inplace=True)

df.plot(x = 'Equipo', y = 'Distancia', kind = 'barh', figsize = (14,10))
plt.show()
# %%
