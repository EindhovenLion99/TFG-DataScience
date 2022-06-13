# %%
import DataFunctions as getdata
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
jugadores, f_riesgo = getdata.read_data('.')

# %%
equipo = "Laguna"
jugadores_equipo = jugadores.loc[jugadores['Equipo'] == equipo].sort_values(['Edad'])
ax_1 = jugadores_equipo.plot.bar(figsize=(15,10), x = 'Jugador', y = 'Edad', xlabel="Jugadores")
ax_1.set_yticks(np.arange(0, max(jugadores_equipo['Edad']) + 2, 1))


# %%
team_total_injuries = jugadores.groupby(['Equipo']).sum()['Total Lesiones'].sort_values()
pl_mean = team_total_injuries.mean()
ax_2 = team_total_injuries.plot(kind = "barh")
ax_2.set_xticks(np.arange(0, max(team_total_injuries) + 2, 2))
ax_2.set(xlabel="Lesiones", title="Numero de lesiones por equipo")
ax_2.axvline(pl_mean, ls="--", color='r')

# %%
pl = jugadores.groupby(['Equipo', 'Posición']).sum()['Total Lesiones'].unstack()
pl = pl.fillna(0)
ax_3 = pl.plot(figsize=(14, 5), kind = "barh", stacked = True)
ax_3.set_xticks(np.arange(0, max(team_total_injuries) + 2, 2))
ax_3.set(xlabel="Lesiones", title="Numero de lesiones por equipo")
ax_3.axvline(pl_mean, ls="--", color='r')


# %%
lesiones = {
  'Pie': {
    'Cantidad': 0,
    'Tobillo': 0,
    'Talón': 0
  },
  'Pierna': {
    'Cantidad': 0,
    'Rodilla': 0,
    'Gemelos': 0,
    'Peroneos': 0,
    'Sóleo': 0,
    'Peroné': 0,
    'Tibia': 0
  },
  'Muslo': {
    'Cantidad': 0,
    'Cuádriceps': 0,
    'Isquiosurales': 0,
    'Adductores': 0
  },
  'Hombro': {
    'Cantidad': 0,
    'Clavícula': 0,
    'Hombro': 0
  },
  'Cadera': {
    'Cantidad': 0,
    'Psoas': 0,
    'Ingle': 0,
    'Glúteo': 0
  },
  'Mano': {
    'Cantidad': 0,
    'Muñeca': 0,
    'Dedos': 0
  },
  'Tronco': {
    'Cantidad': 0,
    'Lumbar': 0
  },
  'Antebrazo': {
    'Cantidad': 0,
    'Muñeca': 0
  },
  'Tórax': {
    'Cantidad': 0,
    'Costillas': 0
  }
}

# %%
lesiones_previas = jugadores['Lesiones Previas']
for row in lesiones_previas:
  if " ; " in row:
    row_array = row.split(" ; ")
    for a in row_array:
      elems = a.split('-')
      if elems[2].capitalize() in lesiones.keys():
        lesiones[elems[2].capitalize()]['Cantidad'] += 1
  elif row != 'No-Sin lesión':
    elems = row.split('-')
    if elems[2].capitalize() in lesiones.keys():
      lesiones[elems[2].capitalize()]['Cantidad'] += 1

lesiones


# %%
