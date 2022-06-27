# %%
import DataFunctions as getdata
import plotFunctions as getplot
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from itertools import combinations

jugadores, f_riesgo = getdata.read_data('.')
completeTable = getdata.combineData2Excel(jugadores, f_riesgo)

# %%
getplot.plotEdadesJugadores("Laguna", jugadores)
getplot.plotEdadesJugadores("Padre Anchieta", jugadores)
getplot.plotEdadesJugadores("Marino", jugadores)

# %%
getplot.plotNumLesionesPorEquipo(jugadores)
getplot.plotNumLesionesPorEquipoAgrupadas(jugadores)

# %%
getplot.plotInjuriesType(lesiones_previas, 'Grupo Muscular', figsize=(10,10), kind='bar')

# %%
lesion_preparacion = getdata.compareInjuriesWith(jugadores, 'Preparación')
getplot.plotCompareWith(lesion_preparacion, figsize=(15,9))


# %%
lesion_preparacion = getdata.compareInjuriesWith(jugadores, 'Escoliosis')
getplot.plotCompareWith(lesion_preparacion, figsize=(15,9))

# %%
lesion_escoliosis = getdata.compareInjuriesWith(jugadores, 'Operaciones')
getplot.plotCompareWith(lesion_escoliosis, figsize=(15,9))

# ---------------------------------------------------------------------------


# %%
lesiones_previas = getdata.getInjuriesTable(jugadores, 'Lesiones Previas', COMBO=True)

# %%
f_riesgo_index = f_riesgo.set_index('Jugador')


# %%
F1 = 'V/V CALCÁNEO'
F2 = '1º DEDO RIG.'
F3 = 'V/V RODILLA'
F4 = 'D. UNIPODAL'
F5 = 'D. BIPODAL'
F6 = 'GL. MEDIO'
F7 = 'ANTE-RETRO'
F8 = 'Sprint'

# %%
getplot.plotFactorRiesgo(f_riesgo, F1)

#%%
data = getdata.combineData2Excel(lesiones_previas, f_riesgo_index)
getplot.plotLesionFactor(data, 'Parte', F8, figsize=(8,15))

# %%
data = getdata.combineData2Excel(lesiones_previas, f_riesgo_index)
getplot.plotFactorRiesgoCombinado(data, [F3, F4, F5], 'Parte')


# %%
vector = [F1, F2, F3, F4, F5, F6, F7, F8]

def cartesian_coord(*arrays):
  grid = np.meshgrid(*arrays)
  coord_list = [entry.ravel() for entry in grid]
  points = np.vstack(coord_list).T
  return points

a = np.arange(4)
print(cartesian_coord(*3*[a]))
print(len(cartesian_coord(*2*[a])))


# %%
list_combinations = list()
for n in range(len(vector) + 1):
  list_combinations += list(combinations(vector, n))

print(len(list_combinations))

for comb in list_combinations:
  if len(comb) == 6:
    getplot.plotFactorRiesgoCombinado(data, [comb[0], comb[1], comb[2], comb[3], comb[4], comb[5]], 'Parte')
# %%
