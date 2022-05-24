
# %% ----------------------
# Fichero con las funciones
import DataFunctions as getdata
import PlotFunctions as getplot
import Statistics as getstats

# %% -- Lectura de los datos
home, away, events = getdata.read_match_data(2)


# %%
getstats.plotTeamStats(events, 'SHOT')

# getstats.plotTeamPosesion(events)

# %%
goals = events.loc[events['Subtype'].str.contains('TARGET-GOAL', na=False)]
START_FRAME = events.loc[goals.index[0]]['Start Frame'] - 25 * 10
print(START_FRAME)

# %%
END_FRAME = START_FRAME + 25 * 60 * 0.5
getplot.clip(home.loc[START_FRAME:END_FRAME], away.loc[START_FRAME:END_FRAME], path='.', PlayerMarkerSize=11)
# %%
