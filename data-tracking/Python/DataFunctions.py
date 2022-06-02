import pandas as pd
import numpy as np
import csv as csv


def read_match_data(game_id, DATADIR):
  home_positions = getGamePositions(game_id, 'Home', DATADIR)
  away_positions = getGamePositions(game_id, 'Away', DATADIR)
  events = getEvents(game_id, DATADIR)
  return home_positions, away_positions, events

def getGamePositions(game_id, team, DATADIR):
  eventfile = DATADIR + '/Sample_Game_%d/Sample_Game_%d_RawTrackingData_%s_Team.csv' % (game_id, game_id, team)
  # eventfile = '../../NewNames/Sample_Game_%d/Sample_Game_%d_RawTrackingData_%s_Team.csv' % (game_id, game_id, team)
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
  positions = getPlayerVel(positions)
  return positions

def getPlayerVel(team, maxspeed = 12):
  player_ids = np.unique( [ c[:-2] for c in team.columns if c[:4] in ['home','away'] ] )
  dt = team['Time [s]'].diff()
  for player in player_ids: # cycle through players individually
    # difference player positions in timestep dt to get unsmoothed estimate of velicity
    vx = team[player + "_x"].diff() / dt
    vy = team[player + "_y"].diff() / dt

    if maxspeed > 0:
        raw_speed = np.sqrt( vx**2 + vy**2 )
        vx[ raw_speed > maxspeed ] = np.nan
        vy[ raw_speed > maxspeed ] = np.nan

    team[player + "_speed"] = np.sqrt( vx**2 + vy**2 )
  return team


def getEvents(game_id, DATADIR):
  eventfile = DATADIR + '/Sample_Game_%d/Sample_Game_%d_RawEventsData.csv' % (game_id, game_id)
  # eventfile = '../../NewNames/Sample_Game_%d/Sample_Game_%d_RawEventsData.csv' % (game_id, game_id)
  events = pd.read_csv(eventfile)
  events = to_metric_coordinates(events)
  events['Minute'] = (events['Start Time [s]'] / 60).astype(int)
  new_index = ['Team', 'Type', 'Subtype', 'Period', 'Minute', 'Start Frame', 'Start Time [s]', 'End Frame', 'End Time [s]',
               'From', 'To', 'Start X', 'Start Y', 'End X', 'End Y']
  events = events.reindex(columns=new_index)
  return events

def to_metric_coordinates(data, field_dimen = (106.,68.)):                      # Tranforma las coordenadas
  x_columns = [c for c in data.columns if c[-1].lower() == 'x']                 # Guardamos las posiciones x
  y_columns = [c for c in data.columns if c[-1].lower() == 'y']                 # Guardamos las posiciones y
  data[x_columns] = round(( data[x_columns]-0.5 ) * field_dimen[0], 2)          # Cambiamos los datos
  data[y_columns] = round(-1 * ( data[y_columns]-0.5 ) * field_dimen[1], 2)

  return data