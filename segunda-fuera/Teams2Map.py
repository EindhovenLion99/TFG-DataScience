# %%
from mpl_toolkits.basemap import Basemap
import matplotlib.pyplot as plt
import csv
import random

# %%
fig = plt.figure(figsize = (60,30))
ax = fig.add_subplot(1,1,1)
ax.set_title("Mapa España")
m = Basemap(ax = ax,
            projection = 'merc',
            llcrnrlat = 27,
            llcrnrlon = -20,
            urcrnrlat = 45,
            urcrnrlon = 5,
            resolution = 'i')

m.drawcoastlines(color = '#324c87')
m.drawcountries(color = '#303338',linewidth = 1)
m.drawmapboundary(fill_color = "#c0eaff")
m.fillcontinents(color = "#ebe7d5", lake_color = "#c0eaff")

with open("CSV/TeamsDistance.csv") as csv_file:
  csv_reader = csv.reader(csv_file, delimiter=',')
  line_count = 0

  team = input("Introduzca el nombre de un equipo de segunda:")

  def plotTeamAndLine(lat1, lon1, lat2, lon2, team2):
    latT, lonT = float(lat1), float(lon1)
    xpt, ypt = m(lonT, latT)
    m.plot(xpt, ypt, marker = 'D', color = 'm')
    xs.append(xpt)
    ys.append(ypt)
    lat, lon = float(lat2), float(lon2)
    xpt, ypt = m(lon, lat)
    m.plot(xpt, ypt, marker = 'D', color = 'm')
    xs.append(xpt)
    ys.append(ypt)
    color = "%06x" % random.randint(0, 0xFFFFFF)
    m.plot(xs, ys, color = '#' + color, linewidth = 2, label = team2)

  for row in csv_reader:
    if line_count == 0:
      line_count += 1
    else:
      xs = []
      ys = []
      if row[0] == team:
        plotTeamAndLine(row[1], row[2], row[4], row[5], row[3])
      elif row[3] == team:
        plotTeamAndLine(row[4], row[5], row[1], row[2], row[0])
        
plt.legend()
plt.title("Basemap")
plt.show()



# %%
