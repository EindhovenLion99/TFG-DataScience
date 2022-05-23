
# %% ----------------------
# Fichero con las funciones
import DataFunctions as getdata
import PlotFunctions as getplot
import Statistics as getstats

# %% -- Lectura de los datos
home, away, events = getdata.read_match_data(2)

# Ejemplo de Jugada
fig, ax = getplot.plot_events(events.loc[1:7], annotate = True)

# %%
getstats.plotTeamStats(events, 'SHOT')

# getstats.plotTeamPosesion(events)

# %%
events.loc[0:10]

# %%
FRAME = events.loc[0]['Start Frame']
getplot.plot_frame(home.loc[FRAME], away.loc[FRAME], PlayerMarkerSize=11)
# %%
