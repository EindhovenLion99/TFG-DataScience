# %%
import DataFunctions as getdata
import plotFunctions as getplot
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

# %%
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
lesiones_previas = getdata.getInjuriesTable(jugadores, 'Lesiones Previas')
lesiones_previas
#getplot.plotInjuriesType(lesiones_previas, 'Grupo Muscular', figsize=(10,15), kind='barh')

# %%
lesion_preparacion = getdata.compareInjuriesWith(jugadores, 'Preparación')
getplot.plotCompareWith(lesion_preparacion, figsize=(15,9))


# %%
lesion_preparacion = getdata.compareInjuriesWith(jugadores, 'Escoliosis')
getplot.plotCompareWith(lesion_preparacion, figsize=(15,9))

# %%
lesion_escoliosis = getdata.compareInjuriesWith(jugadores, 'Operaciones')
getplot.plotCompareWith(lesion_escoliosis, figsize=(15,9))

# %%
getplot.plotFactorRiesgo(f_riesgo, 'GL. MEDIO')


# %%
getplot.plotFactorRiesgoCombinado(f_riesgo, ['V/V CALCÁNEO', 'GL. MEDIO'], ['Valgo ambos', 'Izquierdo'])

# %%
jugadores.corr()
f_riesgo.corr()

# %%
f_riesgo_index = f_riesgo.set_index('Jugador')

#%%
data = getdata.combineData2Excel(lesiones_previas, f_riesgo_index)
getplot.plotLesionFactor(data, 'Lesion', 'V/V CALCÁNEO', figsize=(10,20))
