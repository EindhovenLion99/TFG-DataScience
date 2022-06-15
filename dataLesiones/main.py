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
lesiones_previas = getdata.getInjuriesTable(jugadores)
lesiones_previas

