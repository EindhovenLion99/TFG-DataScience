import csv
from equipo import team
from match import match
from getTeamsWithCity import getTeamsWithCity

teams = getTeamsWithCity('CSV/teams.csv')

with open('CSV/Segunda-20-21-Estadios.csv') as csv_file:
  csv_reader = csv.reader(csv_file, delimiter=',')
  line_count = 0
  for row in csv_reader:
    if line_count == 0:
      line_count += 1         # Ignoramos la primera linea
    else:
      match_ = match(row[0], row[1], row[2], row[3], row[4])   # Guardamos el partido
      for team in teams:
        if (match_.getLocal() == team.name or match_.getAway() == team.name):
          team.setMatch(match_)       # Guardamos el partido al equipo que corresponda
          if not team.estadio and match_.getLocal() == team.name:
            team.setStadium(row[5])
      line_count += 1

  """
  max_away_loses = teams[0].estadisticas['estVisitante']['derrotas']
  for team in teams:
    if team.estadisticas['estVisitante']['derrotas'] > max_away_loses:
      max_away_loses = team.estadisticas['estVisitante']['derrotas']
      max_away_lost_team = team
    
  print(max_away_loses)
  print(max_away_lost_team.name)
  """
  
  for team in teams:
    print("El equipo " + team.name + " tiene como estadio el: " + team.getStadium() + " en la ciudad " + team.ciudad)