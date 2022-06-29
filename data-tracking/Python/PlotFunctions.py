# %%
import pandas as pd
import numpy as np
import csv as csv
import matplotlib.pyplot as plt
from matplotlib.patches import Arc
import matplotlib.animation as animation


def plot_events(events, figax = None, indicators = ['Marker','Arrow'], 
                color = 'r', marker_style = 'o', alpha = 0.5, annotate = False):      # Dibuja el campo
  if figax is None:
    fig, ax = plot_field()
  else:
    fig, ax = figax
  for i, row in events.iterrows():
    if 'Marker' in indicators:
      if row['Team'] == "Home":
        color = "r"
      else:
        color = 'b'
      ax.plot(row['Start X'], row['Start Y'], color + marker_style, alpha = alpha)
    if 'Arrow' in indicators:
      ax.annotate("", xy = row[['End X','End Y']], xytext = row[['Start X','Start Y']], 
                  alpha = alpha, arrowprops = dict(alpha=alpha,width=0.5,headlength=4.0,headwidth=4.0,color=color),
                  annotation_clip = False)
    if annotate:
      textstring = row['From']
      ax.text( row['Start X'], row['Start Y'], textstring, fontsize=10, color = color)
  return fig, ax

def plot_frame(home_team, away_team, colors=('r', 'b'), PlayerMarkerSize=10, PlayerAlpha=0.7, annotate=False, velocity=False, figax=None):
  if figax is None: # create new pitch 
    fig,ax = plot_field()
  else: # overlay on a previously generated pitch
    fig,ax = figax # unpack tuple
  for team,color in zip( [home_team, away_team], colors):
    x_columns = [c for c in team.keys() if c[-2:].lower() == '_x' and c != 'ball_x']
    y_columns = [c for c in team.keys() if c[-2:].lower() == '_y' and c != 'ball_y']
    ax.plot(team[x_columns], team[y_columns], color + 'o', markersize=PlayerMarkerSize, alpha=PlayerAlpha)
    if velocity:
      vx_columns = ['{}_vx'.format(c[:-2]) for c in x_columns]
      vy_columns = ['{}_vy'.format(c[:-2]) for c in y_columns]
      ax.quiver(team[x_columns], team[y_columns], team[vx_columns], team[vy_columns], color=color, scale_units='inches', scale=10, width=0.0015, headlength=5, headwidth=3, alpha=PlayerAlpha)
    if annotate:
      [ ax.text(team[x]+0.5, team[y]+0.5, x.split('_')[1], fontsize=10, color=color  ) for x,y in zip(x_columns,y_columns) if not (np.isnan(team[x]) or np.isnan(team[y]))]
  ax.plot(home_team['ball_x'], home_team['ball_y'], 'ko', alpha=1.0)
  return fig, ax

def clip(home_team, away_team, path, name='clip', fps=25, colors=('r', 'b'), velocity=False, PlayerMarkerSize=10, PlayerAlpha=0.7):
  assert np.all(home_team.index == away_team.index)
  index = home_team.index

  FFMpegWritter = animation.writers['ffmpeg']
  metadata = dict(title = 'Tracking data')
  writer = FFMpegWritter(fps = fps, metadata = metadata)
  filename = path + "/" + name + ".mp4"

  fig, ax = plot_field()
  fig.set_tight_layout(True)
  print("Generating movie...")
  with writer.saving(fig, filename, 100):
    for i in index:
      figObjs = []
      for team,color in zip( [home_team.loc[i], away_team.loc[i]], colors):
        x_columns = [c for c in team.keys() if c[-2:].lower() == '_x' and c != 'ball_x']
        y_columns = [c for c in team.keys() if c[-2:].lower() == '_y' and c != 'ball_y']
        objs, = ax.plot(team[x_columns], team[y_columns], color + 'o', markersize = PlayerMarkerSize, alpha = PlayerAlpha)
        figObjs.append(objs)
        if velocity:
          vx_columns = ['{}_vx'.format(c[:-2]) for c in x_columns]
          vy_columns = ['{}_vy'.format(c[:-2]) for c in y_columns]
          objs = ax.quiver(team[x_columns], team[y_columns], team[vx_columns], team[vy_columns], color=color, scale_units='inches', scale=10, width=0.0015, headlength=5, headwidth=3, alpha=PlayerAlpha)
          figObjs.append(objs)
      objs, = ax.plot(team['ball_x'], team['ball_y'], 'ko', markersize = 6, alpha = 1)
      figObjs.append(objs)

      frame_minute = int(team['Time [s]'] / 60)
      frame_second = (team['Time [s]'] / 60 - frame_minute) * 60
      time = "%d:%1.2f" % (frame_minute, frame_second)
      objs = ax.text(-2.5, 54, time, fontsize = 14)
      figObjs.append(objs)
      writer.grab_frame()
      for figobj in figObjs:
        figobj.remove()

  print("Done")
  plt.clf()
  plt.close(fig)

def plot_field(fig_size=(11, 7)):
  #Create figure
  fig, ax = plt.subplots(figsize=fig_size)
  ax.set_facecolor('mediumseagreen')

  #Pitch Outline & Centre Line
  ax.plot([0,0],[-34,34], color="white")
  ax.plot([-53,53],[34,34], color="white")
  ax.plot([-53,53],[-34,-34], color="white")
  ax.plot([-53,-53],[-34,34], color="white")
  ax.plot([53,53],[-34,34], color="white")


  #Left Penalty Area
  ax.plot([-53,-36.5],[-20.41,-20.41],color="white")
  ax.plot([-53,-36.5],[20.41,20.41],color="white")
  ax.plot([-36.5,-36.5],[-20.41,20.41],color="white")


  #Right Penalty Area
  ax.plot([36.5,36.5],[-20.41,20.41],color="white")
  ax.plot([36.5,53],[-20.41,-20.41],color="white")
  ax.plot([36.5,53],[20.41,20.41],color="white")


  #Left 6-yard Box
  ax.plot([-53,-47.5],[9.16, 9.16],color="white")
  ax.plot([-53,-47.5],[-9.16,-9.16],color="white")
  ax.plot([-47.5,-47.5],[-9.16,9.16],color="white")

  # Goal Left

  ax.plot([-53, -54], [-3.66, -3.66], color="white")
  ax.plot([-53, -54], [3.66, 3.66], color="white")
  ax.plot([-54, -54], [3.66, -3.66], color="white")

  # Goal Right

  ax.plot([53, 54], [-3.66, -3.66], color="white")
  ax.plot([53, 54], [3.66, 3.66], color="white")
  ax.plot([54, 54], [3.66, -3.66], color="white")


  #Right 6-yard Box
  ax.plot([47.5,53],[9.16,9.16],color="white")
  ax.plot([47.5,53],[-9.16, -9.16],color="white")
  ax.plot([47.5,47.5],[-9.16, 9.16],color="white")


  #Prepare Circles
  centreCircle = plt.Circle((0,0),9.15,color="white",fill=False)
  centreSpot = plt.Circle((0,0),0.8,color="white")
  leftPenSpot = plt.Circle((-42,-0),0.8,color="white")
  rightPenSpot = plt.Circle((42,0),0.8,color="white")

  #Draw Circles
  ax.add_patch(centreCircle)
  ax.add_patch(centreSpot)
  ax.add_patch(leftPenSpot)
  ax.add_patch(rightPenSpot)


  #Prepare Arcs
  leftArc = Arc((-42,0),height=18.3,width=18.3,angle=0,theta1=310,theta2=50,color="white")
  rightArc = Arc((42,0),height=18.3,width=18.3,angle=0,theta1=130,theta2=230,color="white")

  #Draw Arcs
  ax.add_patch(leftArc)
  ax.add_patch(rightArc)

  #Tidy Axes
  ax.axis('on')
  return fig, ax

def plot_minutes_played(team, team_str):
  team_str = team_str.lower()
  players = np.unique([c.split('_')[1] + "_" + c.split('_')[2] for c in team.columns if c[:4] == team_str])
  player_summary = pd.DataFrame(index = players)

  minutes = []

  for pl in players:
    column = team_str + '_' + pl + '_x'
    pl_minutes = (team[column].last_valid_index() - team[column].first_valid_index() + 1) / 25 / 60
    minutes.append(pl_minutes)

  player_summary['Minutes Played'] = minutes
  player_summary = player_summary.sort_values(['Minutes Played'], ascending = False)

  player_summary['Minutes Played'].plot.bar(figsize=(10,8))

def plot_total_distance(team, team_str):
  team_str = team_str.lower()
  players = np.unique([c.split('_')[1] + "_" + c.split('_')[2] for c in team.columns if c[:4] == team_str])
  player_summary = pd.DataFrame(index = players)

  distance = []

  for pl in players:
    column = team_str + '_' + pl + '_speed'
    pl_distance = team[column].sum() / 25 / 1000
    distance.append(pl_distance)

  player_summary['Total Distance'] = distance
  player_summary = player_summary.sort_values(['Total Distance'], ascending = False)

  player_summary['Total Distance'].plot.bar(figsize=(10,8))


def plot_type_distance_covered(team, team_str):
  walking = []
  jogging = []
  running = []
  sprinting = []

  team_str = team_str.lower()
  players = np.unique([c.split('_')[1] + "_" + c.split('_')[2] for c in team.columns if c[:4] == team_str])
  player_summary = pd.DataFrame(index = players)

  for pl in players:
    column = team_str + "_" + pl + "_speed"
    player_dist = team.loc[team[column] < 2, column].sum() / 25 / 1000
    walking.append(player_dist)
    player_dist = team.loc[(team[column] >= 2) & (team[column] < 4), column].sum() / 25 / 1000
    jogging.append(player_dist)
    player_dist = team.loc[(team[column] >= 4) & (team[column] < 7), column].sum() / 25 / 1000
    running.append(player_dist)
    player_dist = team.loc[team[column] >= 7, column].sum() / 25 / 1000
    sprinting.append(player_dist)

  player_summary['Walking'] = walking
  player_summary['Jogging'] = jogging
  player_summary['Running'] = running
  player_summary['Sprinting'] = sprinting

  ax = player_summary[['Walking','Jogging','Running','Sprinting']].plot.bar(colormap='coolwarm')
  ax.set_xlabel('Player')
  ax.set_ylabel('Distance covered')





def plot_pitch_control_for_event(event_id, events, home, away, PPCF, xgrid, ygrid, alpha = 0.7, include_player_velocities=True, annotate=True):
  pass_frame = events.loc[event_id]['Start Frame']
  pass_team = events.loc[event_id].Team

  fig, ax = plot_field()
  plot_frame(home.loc[pass_frame], away.loc[pass_frame], figax=(fig,ax), PlayerAlpha=alpha, velocity=include_player_velocities, annotate=annotate)
  plot_events(events.loc[event_id:event_id], figax=(fig,ax), annotate=False, color='k', alpha=1)

  if pass_team == 'Home':
    cmap = 'bwr'
  else:
    cmap = 'bwr_r'

  ax.imshow(np.flipud(PPCF), extent=(-106/2., 106/2., -68/2., 68/2.), interpolation='spline36', vmin=0.0, vmax=1.0, cmap=cmap, alpha=0.5)
  return fig,ax