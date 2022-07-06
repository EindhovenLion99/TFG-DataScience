
# %% ----------------------
# Fichero con las funciones
import DataFunctions as getdata
import PlotFunctions as getplot
import Statistics as getstats
import pandas as pd
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
from sklearn.cluster import KMeans
import matplotlib.pyplot as plt
import numpy as np

home_passes = events[ (events['Type'].isin(['PASS'])) & (events['Team']=='Away') ]

# list for storing pass probablities
pass_success_probability = []

for i,row in home_passes.iterrows():
    pass_start_pos = np.array([row['Start X'],row['Start Y']])
    pass_target_pos = np.array([row['End X'],row['End Y']])
    pass_frame = row['Start Frame']
    
    attacking_players = getpitchcontrol.initialise_players(away.loc[pass_frame],'away',getpitchcontrol.default_params())
    defending_players = getpitchcontrol.initialise_players(home.loc[pass_frame],'home',getpitchcontrol.default_params())
    Patt,Pdef = getpitchcontrol.calculate_pitch_control_at_target(pass_target_pos, attacking_players, defending_players, pass_start_pos, getpitchcontrol.default_params())

    pass_success_probability.append( (i,Patt) )
    
import matplotlib.pyplot as plt
fig,ax = plt.subplots()
ax.hist( [p[1] for p in pass_success_probability], np.arange(0,1.1,0.1))    
ax.set_xlabel('Pass success probability')
ax.set_ylabel('Frequency')  







# %%

eventfile = '../Sample_Game_1/EditedEvents.csv'

events = pd.read_csv(eventfile)
new_index = ['Team', 'Type', 'Subtype', 'Period', 'Minute', 'Start Frame', 'Start Time [s]', 'End Frame', 'End Time [s]',
              'From', 'To', 'Start X', 'Start Y', 'End X', 'End Y']
events = events.reindex(columns=new_index)
events = events.loc[events['Type'] == 'PASS']
events = events.drop(columns = ['Team', 'Type', 'Subtype', 'Period', 'Minute', 'Start Frame', 'Start Time [s]', 'End Frame', 'End Time [s]'])
events.reset_index(drop = True, inplace = True)
events.describe()

wcss = []

for i in range(1, 11):
  kmeans = KMeans(n_clusters=i)
  kmeans.fit(events)
  wcss.append(kmeans.inertia_)

plt.plot(range(1,11), wcss)
plt.title("Codo")
plt.xlabel("Numero de clusters")
plt.ylabel('WCSS')
plt.show()

clustering = KMeans(n_clusters=4, max_iter=300)
clustering.fit(events)

events['KMeans_Cluster'] = clustering.labels_
events.head()

from sklearn.decomposition import PCA

pca = PCA(n_components=2)
pca_events = pca.fit_transform(events)
pca_events_df = pd.DataFrame(data = pca_events, columns = ['Component_1', 'Component_2'])
pca_nombre_events = pd.concat([pca_events_df, events[['KMeans_Cluster']]], axis = 1)

pca_nombre_events

fig = plt.figure(figsize=(6, 6))
ax = fig.add_subplot(1,1,1)
ax.set_xlabel('Componente 1', fontsize = 15)
ax.set_ylabel('Componente 2', fontsize = 15)
ax.set_title('Componentes Principales', fontsize = 20)

color_theme = np.array(['blue', 'green', 'orange', 'red'])
ax.scatter(x = pca_nombre_events.Component_1, y = pca_nombre_events.Component_2, c=color_theme[pca_nombre_events.KMeans_Cluster], s = 50)
plt.show()
# %%
