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
lesiones = [{
  'Pie': {
    'Cantidad': 0,
    'Tobillo': 0
  },
  'Pierna': {
    'Cantidad': 0,
    
  }
}]