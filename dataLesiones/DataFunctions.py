import pandas as pd
import numpy as np
import csv as csv

def read_data(DATADIR):
  file = DATADIR + '/TablaJugadores.csv'
  file2 = DATADIR + '/TablaFactorRiesgo.csv'
  jugadores = read_csv_file(file)
  f_riesgo = read_csv_file(file2)
  return jugadores, f_riesgo


def read_csv_file(file):
  player_info = pd.read_csv(file)
  return player_info

