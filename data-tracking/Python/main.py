
# %% ----------------------
# Fichero con las funciones
import DataFunctions as getdata
import PlotFunctions as getplot
import Statistics as getstats
dir = '../../NewNames'

# %% -- Lectura de los datos
home, away, events = getdata.read_match_data(2, dir)

# %%
getstats.plotTeamPosesion(events)
 # %%
getplot.plot_frame(home.iloc[51], away.iloc[51], annotate=True)

# %%
goals = events.loc[events['Subtype'].str.contains('TARGET-GOAL', na=False)]
START_FRAME = events.loc[goals.index[0]]['Start Frame'] - 25 * 10
END_FRAME = START_FRAME + 25 * 60 * 0.5
getplot.clip(home.loc[START_FRAME:END_FRAME], away.loc[START_FRAME:END_FRAME], path='.', PlayerMarkerSize=11)


# %%
getplot.plot_minutes_played(home, 'home')


# %%
getplot.plot_minutes_played(away, 'away')
