# %%
import DataFunctions as getdata
import plotFunctions as getplot
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

# %%
jugadores, f_riesgo = getdata.read_data('.')
#completeTable = getdata.combineData2Excel(jugadores, f_riesgo)

# %%
getplot.plotEdadesJugadores("Laguna", jugadores)
getplot.plotEdadesJugadores("Padre Anchieta", jugadores)
getplot.plotEdadesJugadores("Marino", jugadores)

# %%
getplot.plotNumLesionesPorEquipo(jugadores)

# %%
getplot.plotNumLesionesPorEquipoAgrupadas(jugadores)

# %%
lesiones_previas = getdata.getInjuriesTable(jugadores)
lesiones_previas

