
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

def plotEdadesJugadores(equipo, jugadores):
  jugadores_equipo = jugadores.loc[jugadores['Equipo'] == equipo].sort_values(['Edad'])
  ax_1 = jugadores_equipo.plot.bar(figsize=(15,10), use_index=True, y = 'Edad', xlabel="Jugadores")
  ax_1.set_yticks(np.arange(0, max(jugadores_equipo['Edad']) + 2, 1))

def plotNumLesionesPorEquipo(jugadores):
  team_total_injuries = jugadores.groupby(['Equipo']).sum()['Total Lesiones'].sort_values()
  pl_mean = team_total_injuries.mean()
  ax_2 = team_total_injuries.plot(kind = "barh")
  ax_2.set_xticks(np.arange(0, max(team_total_injuries) + 2, 2))
  ax_2.set(xlabel="Lesiones", title="Numero de lesiones por equipo")
  ax_2.axvline(pl_mean, ls="--", color='r')

def plotNumLesionesPorEquipoAgrupadas(jugadores):
  pl = jugadores.groupby(['Equipo', 'Posición']).sum()['Total Lesiones'].unstack()
  team_total_injuries = jugadores.groupby(['Equipo']).sum()['Total Lesiones']
  pl_mean = team_total_injuries.mean()
  pl = pl.fillna(0)
  ax_3 = pl.plot(figsize=(14, 5), kind = "barh", stacked = True)
  ax_3.set_xticks(np.arange(0, max(team_total_injuries) + 2, 2))
  ax_3.set(xlabel="Lesiones", title="Numero de lesiones por equipo")
  ax_3.axvline(pl_mean, ls="--", color='r')

def plotInjuriesType(lesiones, tipo, figsize=(10,8), kind='bar'):
  lesiones['Grupo Muscular'] = lesiones['Vector Lesiones'].str.split('-').str[-1]
  lesiones['Parte'] = lesiones['Vector Lesiones'].str.split('-').str[1]
  lesiones['Lesion'] = lesiones['Vector Lesiones'].str.split('-').str[0]
  lesiones = lesiones.drop(lesiones[lesiones.Lesion == 'No'].index)

  lesiones = lesiones.groupby(tipo)['Lesion'].count()
  ax_4 = lesiones.plot(legend=False, kind=kind, figsize=figsize)
  if (kind == 'barh'):
    ax_4.set_xticks(np.arange(0, max(lesiones) + 2, 2))
  else:
    ax_4.set_yticks(np.arange(0, max(lesiones) + 2, 2))


def plotCompareWith(data, figsize=(10,8)):
  ax_5 = data.plot(kind='bar', figsize=figsize)
  ax_5.set_yticks(np.arange(0, max(data['Total de Jugadores']) + 2, 2))
  for container in ax_5.containers:
    ax_5.bar_label(container)


def plotFactorRiesgo(f_riesgo, factor, tipo=False):
  if tipo:
    jugadores = f_riesgo.loc[f_riesgo[factor] == tipo, ['Jugador', 'Equipo']]
  else:
    jugadores = f_riesgo.loc[f_riesgo[factor] != "No", ['Jugador', 'Equipo', factor]]
  print(jugadores)
  f_ = f_riesgo[factor].value_counts()
  f_.plot(kind='bar')

def plotFactorRiesgoCombinado(f_riesgo, factores, tipos):
  print(factores)
  print(tipos)
  if tipos:
    jugadores = f_riesgo.loc[(f_riesgo[factores[0]] == tipos[0]) & (f_riesgo[factores[1]] == tipos[1]), ['Jugador', 'Equipo', factores[0], factores[1]]]
  print(jugadores)