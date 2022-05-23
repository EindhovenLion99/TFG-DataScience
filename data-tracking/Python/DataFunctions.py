# %%
import pandas as pd
import csv as csv

#  %%

def read_match_data(game_id):
  home_positions = getGamePositions(game_id, 'Home')
  away_positions = getGamePositions(game_id, 'Away')
  events = getEvents(game_id)
  return home_positions, away_positions, events

# %%
def getGamePositions(game_id, team):
  eventfile = '../Sample_Game_%d/Sample_Game_%d_RawTrackingData_%s_Team.csv' % (game_id, game_id, team)
  csvfile = open(eventfile, 'r')
  reader = csv.reader(csvfile)
  team = next(reader)[3].lower()

  team_numbers = [number for number in next(reader) if number != '']
  columns = next(reader)

  for i, j in enumerate(team_numbers):
    columns[i * 2 + 3] = team + "_" + j + "_x"
    columns[i * 2 + 4] = team + "_" + j + "_y"

  columns[-2] = "ball_x"
  columns[-1] = "ball_y"

  positions = pd.read_csv(eventfile, names = columns, index_col = 'Frame', skiprows = 3)
  positions = to_metric_coordinates(positions)
  return positions

# %%

def getEvents(game_id):
  eventfile = '../Sample_Game_%d/Sample_Game_%d_RawEventsData.csv' % (game_id, game_id)
  events = pd.read_csv(eventfile)
  events = to_metric_coordinates(events)
  return events

def to_metric_coordinates(data, field_dimen = (106.,68.)):                      # Tranforma las coordenadas
  x_columns = [c for c in data.columns if c[-1].lower() == 'x']                 # Guardamos las posiciones x
  y_columns = [c for c in data.columns if c[-1].lower() == 'y']                 # Guardamos las posiciones y
  data[x_columns] = round(( data[x_columns]-0.5 ) * field_dimen[0], 2)          # Cambiamos los datos
  data[y_columns] = round(-1 * ( data[y_columns]-0.5 ) * field_dimen[1], 2)

  return data