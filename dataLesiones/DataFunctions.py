import pandas as pd
import numpy as np
import csv as csv

def read_data(DATADIR):
  file = DATADIR + '/TablaJugadores.csv'
  file2 = DATADIR + '/TablaFactorRiesgo.csv'
  jugadores = read_csv_file(file)
  f_riesgo = read_csv_file(file2)
  jugadores = jugadores.set_index('Jugador')
  return jugadores, f_riesgo


def read_csv_file(file):
  player_info = pd.read_csv(file)
  return player_info

def combineData2Excel(jugadores, f_riesgo):
  combinedTables = pd.merge(jugadores, f_riesgo, left_index=True, right_index=True)
  completeTable = combinedTables.drop(columns=['Equipo_y'])
  completeTable.columns = completeTable.columns.str.replace('_x', '')
  #completeTable.to_excel('TablaCompelta.xlsx')
  return combinedTables

def getInjuriesTable(jugadores, periodo_lesion):
  lesiones_previas = jugadores[['Equipo', 'Edad', 'Altura', periodo_lesion]]
  lesiones_previas['Vector Lesiones'] = lesiones_previas[periodo_lesion].str.split(" ; ")
  lesiones_previas = lesiones_previas.explode('Vector Lesiones')
  lesiones_previas['Lesion'] = lesiones_previas['Vector Lesiones'].str.split("-").str[0]
  lesiones_previas['Parte'] = lesiones_previas['Vector Lesiones'].str.split("-").str[1]
  lesiones_previas['Grupo Muscular'] = lesiones_previas['Vector Lesiones'].str.split("-").str[-1]
  lesiones_previas = lesiones_previas.drop(columns=[periodo_lesion])
  lesiones_previas = lesiones_previas.drop(columns=['Vector Lesiones'])
  return lesiones_previas

def compareInjuriesWith(jugadores, parameter='Preparación'):
  if parameter == 'Operaciones':
    jugadores_preparacion = jugadores.loc[jugadores['Operaciones'] != 'No'].groupby('Equipo', as_index=False)[parameter].count()
  else:
    jugadores_preparacion = jugadores.groupby('Equipo', as_index=False)[parameter].sum()
  equipos = jugadores.groupby('Equipo', as_index=False)['Edad'].sum()
  juagdores_total = jugadores.groupby('Equipo', as_index=False).count()
  jugadores_lesionados = jugadores.loc[jugadores['Total Lesiones'] > 0].groupby('Equipo', as_index=False).count()
  

  new_data = pd.DataFrame()
  new_data['Equipo'] = equipos['Equipo']
  new_data['Total de Jugadores'] = juagdores_total['Total Lesiones']
  new_data['Jugadores Lesionados'] = jugadores_lesionados['Total Lesiones']
  new_string = 'Jugadores con ' + parameter
  new_data[new_string] = jugadores_preparacion[parameter]
  new_data = new_data.set_index('Equipo')
  return new_data

