
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

def plotEdadesJugadores(equipo, jugadores, figsize=(10,8)):

  jugadores_equipo = jugadores.loc[jugadores['Equipo'] == equipo].sort_values(['Edad'])
  ax_1 = jugadores_equipo.plot.barh(figsize=figsize, use_index=True, y = 'Edad', xlabel="Jugadores")
  ax_1.set_title("Clasificacion de edad del " + equipo)
  ax_1.set_xticks(np.arange(0, max(jugadores_equipo['Edad']) + 2, 1))

def plotNumLesionesPorEquipo(jugadores, tipo):
  team_total_injuries = jugadores.groupby(['Equipo']).sum()[tipo].sort_values()
  print(team_total_injuries)
  pl_mean = team_total_injuries.mean()
  ax_2 = team_total_injuries.plot(kind = "barh")
  ax_2.set_xticks(np.arange(0, max(team_total_injuries) + 2, 2))
  ax_2.set(xlabel="Lesiones", title="Numero de lesiones por equipo")
  ax_2.axvline(pl_mean, ls="--", color='r')
  ax_2.set_title("Lesiones por equipo (" + tipo + ")")

def plotNumLesionesPorEquipoAgrupadas(jugadores, tipo):
  pl = jugadores.groupby(['Equipo', 'Posición']).sum()[tipo].unstack()
  team_total_injuries = jugadores.groupby(['Equipo']).sum()[tipo]
  pl_mean = team_total_injuries.mean()
  pl = pl.fillna(0)
  ax_3 = pl.plot(figsize=(14, 5), kind = "barh", stacked = True)
  ax_3.set_xticks(np.arange(0, max(team_total_injuries) + 2, 2))
  ax_3.set(xlabel="Lesiones", title="Numero de lesiones por equipo")
  ax_3.axvline(pl_mean, ls="--", color='r')
  ax_3.set_title("Lesiones por equipo agrupadas (" + tipo + ")")

def plotLesionFactor(jugadores, tipo, factor, figsize, mixed=False):
  if mixed:
    #jugadores = jugadores.loc[jugadores[factor] != 'No', factor] = 'Si'
    jugadores[factor] = ['Si' if valor != 'No' and valor != 'Normal' and valor != 'Neutro' else valor for valor in jugadores[factor]]
  pl = jugadores.groupby([tipo, factor])[factor].count().unstack()
  ax_ = pl.plot(figsize=figsize, kind = "barh", stacked = True)
  for c in ax_.containers:
    labels = [int(v.get_width()) if v.get_width() > 0 else '' for v in c]
    ax_.bar_label(c, labels=labels, label_type='center')

def plotInjuriesType(lesiones, tipo, figsize=(10,8), kind='bar'):
  lesiones['Parte'] = lesiones['Vector Lesiones'].str.split('-').str[-1]
  lesiones['Grupo Muscular'] = lesiones['Vector Lesiones'].str.split('-').str[1]
  lesiones['Lesion'] = lesiones['Vector Lesiones'].str.split('-').str[0]
  lesiones = lesiones.drop(lesiones[lesiones.Lesion == 'No'].index)

  lesiones = lesiones.groupby(tipo)['Lesion'].count()
  ax_4 = lesiones.plot(legend=False, kind=kind, figsize=figsize)
  if (kind == 'barh'):
    ax_4.set_xticks(np.arange(0, max(lesiones) + 2, 2))
  else:
    ax_4.set_yticks(np.arange(0, max(lesiones) + 2, 2))
  for container in ax_4.containers:
    ax_4.bar_label(container)
  ax_4.set_title('Numero de lesiones (Lesiones Previas)')


def plotCompareWith(data, figsize=(10,8)):
  ax_5 = data.plot(kind='bar', figsize=figsize)
  ax_5.set_yticks(np.arange(0, max(data['Total de Jugadores']) + 2, 2))
  for container in ax_5.containers:
    ax_5.bar_label(container)


def plotFactorRiesgo(f_riesgo, factor, tipo=False, kind='bar'):
  if tipo:
    jugadores = f_riesgo.loc[f_riesgo[factor] == tipo, ['Jugador', 'Equipo']]
  else:
    jugadores = f_riesgo.loc[f_riesgo[factor] != "No", ['Jugador', 'Equipo', factor]]
  print(jugadores)
  f_ = f_riesgo[factor].value_counts()
  ax = f_.plot(kind=kind)
  for container in ax.containers:
    ax.bar_label(container)
  ax.set_title(factor)


def label_race(row, factores):
  count = 0
  for fact in factores:
    if row[fact] == 'Si':
      count += 1
  if count == len(factores):
    return 'Si'
  else:
    return 'No'

def plotFactorRiesgoCombinado(jugadores, factores, zona, figsize=(10,15)):
  new_string = ""
  for factor in factores:
    new_string += factor + " "
    jugadores[factor] = ['Si' if valor != 'No' and valor != 'Normal' and valor != 'Neutro' else valor for valor in jugadores[factor]]
  jugadores[new_string] = jugadores.apply(lambda row: label_race(row, factores), axis=1)
  pl = jugadores.groupby([zona, new_string])[new_string].count().unstack()
  ax_ = pl.plot(figsize=figsize, kind = "barh", stacked = True)
  for c in ax_.containers:
    labels = [int(v.get_width()) if v.get_width() > 0 else '' for v in c]
    ax_.bar_label(c, labels=labels, label_type='center')
  

def plotCorrelatividad(jugadores, var1, var2):
  f = plt.figure(figsize=(19,15))
  plt.matshow(jugadores.corr(), fignum=f.number)
  plt.xticks(np.arange(min(jugadores['Edad']), max(jugadores['Edad']), 1), fontsize=14, rotation=45)
  plt.yticks(np.arange(min(jugadores['Total Lesiones']), max(jugadores['Total Lesiones']), 1), fontsize=14)
  cb = plt.colorbar()
  cb.ax.tick_params(labelsize=14)
  plt.title('Correlation Matriz', fontsize=16);
