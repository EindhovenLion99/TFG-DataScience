# %%
import pandas as pd
import csv as csv
import matplotlib.pyplot as plt
from matplotlib.patches import Arc


def plot_events(events, figax = None, indicators = ['Marker','Arrow'], 
                color = 'r', marker_style = 'o', alpha = 0.5, annotate = False):      # Dibuja el campo

  if figax is None:
    fig, ax = plot_field()
  else:
    fig, ax = figax
  for i, row in events.iterrows():
    if 'Marker' in indicators:
      ax.plot(row['Start X'], row['Start Y'], color + marker_style, alpha = alpha)
    if 'Arrow' in indicators:
      ax.annotate("", xy = row[['End X','End Y']], xytext = row[['Start X','Start Y']], 
                  alpha = alpha, arrowprops = dict(alpha=alpha,width=0.5,headlength=4.0,headwidth=4.0,color=color),
                  annotation_clip = False)
    if annotate:
      textstring = row['From']
      ax.text( row['Start X'], row['Start Y'], textstring, fontsize=10, color = color)
  return fig, ax

def plot_frame(home_team, away_team, colors=('r', 'b'), PlayerMarkerSize=10, PlayerAlpha=0.7, annotate=False):
  fig, ax = plot_field()
  for team,color in zip( [home_team, away_team], colors):
    x_columns = [c for c in team.keys() if c[-2:].lower() == '_x' and c != 'ball_x']
    y_columns = [c for c in team.keys() if c[-2:].lower() == '_y' and c != 'ball_y']
    ax.plot(team[x_columns], team[y_columns], color + 'o', markersize=PlayerMarkerSize, alpha=PlayerAlpha)
  
  ax.plot(home_team['ball_x'], home_team['ball_y'], 'ko', alpha=1.0)
  return fig, ax

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
