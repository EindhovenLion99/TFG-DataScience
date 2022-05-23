from getCitiesLocation import getDistance
import csv
from Clases.team import team
from getTeamsWithCity import getTeamsWithCity

teams = getTeamsWithCity('CSV/teams.csv')

f = open('CSV/TeamsDistance.csv', 'w')
L = ['"City1","lat","lon","City2","lat","lon","Distance"' + '\n']
f.writelines(L)
for i in range(len(teams)):
  for j in range(len(teams)):
    if j > i:
      data = getDistance(teams[i], teams[j])
      L = ['"' + teams[i].name + '","' + str(data["coord1"]["lat"]) + '","' + str(data["coord1"]["lon"]) 
         + '","' + teams[j].name + '","' + str(data["coord2"]["lat"]) + '","' + str(data["coord2"]["lon"]) 
         + '","' + str(data["distance"]) + '"\n']
      f.writelines(L)

