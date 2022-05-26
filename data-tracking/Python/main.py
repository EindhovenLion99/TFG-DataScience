
# %% ----------------------
# Fichero con las funciones
import DataFunctions as getdata
import PlotFunctions as getplot
import Statistics as getstats

# %% -- Lectura de los datos
home, away, events = getdata.read_match_data(2)

# %%
goals = events.loc[events['Subtype'].str.contains('TARGET-GOAL', na=False)]

# %%
fig, ax = getplot.plot_field()
ax.plot(home['home_10_x'].iloc[:1500], home['home_10_y'].iloc[:1500], 'r', markersize = 1)

# %%
START_FRAME = events.loc[goals.index[0]]['Start Frame'] - 25 * 10
print(START_FRAME)

# %%
END_FRAME = START_FRAME + 25 * 60 * 0.5
getplot.clip(home.loc[START_FRAME:END_FRAME], away.loc[START_FRAME:END_FRAME], path='.', PlayerMarkerSize=11)
