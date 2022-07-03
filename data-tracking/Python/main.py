
# %% ----------------------
# Fichero con las funciones
import DataFunctions as getdata
import PlotFunctions as getplot
import Statistics as getstats
import PitchControl_copy as getpitchcontrol
dir = '../../NewNames'

# %% -- Lectura de los datos
home, away, events = getdata.read_match_data(2, dir)

# %%
getstats.plotTeamPosesion(events, figsize=(8,8))

# %%
getstats.plotTeamStats(events, 'SET PIECE', 'THROW IN')

# %%
getplot.plot_events(events.loc[(events['Type'] == 'SHOT') & (events['Team'] == 'Home') & (events['Subtype'] == 'ON TARGET-GOAL')])

# %%
getplot.plot_frame(home.iloc[2654], away.iloc[2654], annotate=True, velocity=True)


# %%
getplot.plot_type_distance_covered(home, 'home', figsize=(15,10))

# %%
goals = events.loc[events['Subtype'].str.contains('TARGET-GOAL', na=False)]
START_FRAME = events.loc[goals.index[1]]['Start Frame'] - 25 * 10
END_FRAME = START_FRAME + 25 * 60 * 0.25
getplot.clip(home.loc[START_FRAME:END_FRAME], away.loc[START_FRAME:END_FRAME], path='.', PlayerMarkerSize=11, velocity=True)


# %%
getplot.plot_minutes_played(home, 'home')
getplot.plot_minutes_played(away, 'away')
getplot.plot_type_distance_covered(home, 'home')

# %%
shots = events[events['Type'] == 'SHOT']
goals = shots[shots['Subtype'].str.contains('-GOAL')].copy()


getplot.plot_events(events.loc[820:823], annotate=True)

# %%
getplot.plot_frame(home.iloc[820], away.iloc[820])

# %%
params = getpitchcontrol.default_params()

PPCF, xgrid, ygrid = getpitchcontrol.generate_pitch_control(820, events, home, away, params, n_grid_cells_x=50)

# %%
getplot.plot_pitch_control_for_event( 820, events, home, away, PPCF, xgrid, ygrid, annotate=True )
# %%
