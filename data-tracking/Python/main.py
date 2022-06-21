
# %% ----------------------
# Fichero con las funciones
import DataFunctions as getdata
import PlotFunctions as getplot
import Statistics as getstats
import PitchControl as getpitchcontrol
dir = '../../NewNames'

# %% -- Lectura de los datos
home, away, events = getdata.read_match_data(2, dir)

# %%
home
# %%
getstats.plotTeamPosesion(events)
getplot.plot_frame(home.iloc[2891], away.iloc[2891], annotate=True, velocity=True)


# %%
goals = events.loc[events['Subtype'].str.contains('TARGET-GOAL', na=False)]
START_FRAME = events.loc[goals.index[0]]['Start Frame'] - 25 * 10
END_FRAME = START_FRAME + 25 * 60 * 0.25
getplot.clip(home.loc[START_FRAME:END_FRAME], away.loc[START_FRAME:END_FRAME], path='.', PlayerMarkerSize=11, velocity=True, annotate=True)


# %%
getplot.plot_minutes_played(home, 'home')
getplot.plot_minutes_played(away, 'away')
getplot.plot_type_distance_covered(home, 'home')

# %%
shots = events[events['Type'] == 'SHOT']
goals = shots[shots['Subtype'].str.contains('-GOAL')].copy()


getplot.plot_events(events.loc[goals.index[1] - 3 : goals.index[1]], annotate=True)

# %%
params = getpitchcontrol.default_params()