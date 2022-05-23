import csv
from Clases.team import team

def getTeamsWithCity(file):
  with open(file) as csv_file:
    teams = []
    csv_reader = csv.reader(csv_file, delimiter=',')
    line_count = 0
    for row in csv_reader:
      if line_count == 0:
        line_count += 1
      else:
        teams.append(team(row[0], row[1]))
    return teams