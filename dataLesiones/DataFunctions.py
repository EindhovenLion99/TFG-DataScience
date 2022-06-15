import pandas as pd
import numpy as np
import csv as csv

def read_data(DATADIR):
  file = DATADIR + '/TablaJugadores.csv'
  file2 = DATADIR + '/TablaFactorRiesgo.csv'
  jugadores = read_csv_file(file)
  f_riesgo = read_csv_file(file2)
  jugadores = jugadores.set_index('Jugador')
  f_riesgo = f_riesgo.set_index('Jugador')
  return jugadores, f_riesgo


def read_csv_file(file):
  player_info = pd.read_csv(file)
  return player_info

def combineData2Excel(jugadores, f_riesgo):
  combinedTables = pd.merge(jugadores, f_riesgo, left_index=True, right_index=True)
  completeTable = combinedTables.drop(columns=['Equipo_y'])
  completeTable.columns = completeTable.columns.str.replace('_x', '')
  completeTable.to_excel('TablaCompelta.xlsx')
  return combinedTables

def getInjuriesTable(jugadores):
  lesiones_previas = jugadores[['Equipo', 'Edad', 'Altura', 'Lesiones Previas']]
  lesiones_previas['Vector Lesiones'] = lesiones_previas['Lesiones Previas'].str.split(" ; ")
  lesiones_previas = lesiones_previas.explode('Vector Lesiones')
  lesiones_previas = lesiones_previas.drop(columns=['Lesiones Previas'])
  return lesiones_previas

