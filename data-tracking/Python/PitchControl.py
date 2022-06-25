import numpy as np

def default_params():
  params = {}

  # Parametros del modelo

  params['PlayerMaxAcl'] = 7.0                    # Aceleracion maxima de un jugador 7 m/s^2
  params['PlayerMaxSpd'] = 5.0                    # Velocidad maxima de un jugador 5 m/s

  params['PlayerReactTime'] = 0.7                 # Tiempo medio que tarda un jugador en reaccionar
  params['sigma'] = 0.45                          # Desviacion estandar de Spearman 2018
  params['KappaDef'] = 1.                         # Parametro Kappa que da ventaja a los defensas en controlar el balon (es 1.72 pero pongo 1)
  params['LambdaAtt'] = 4.3                       # Parametro Lambda de controlar el balon por parte del equipo atacante
  params['LambdaDef'] = 4.3 * params['KappaDef']  # Parametro Lambda para los defensores

  params['BallSpd'] = 15.                         # Velocidad del balon (15 m/s) aproximada

  # Parametros de evaluacion del modelo

  params['int_dt'] = 0.04
  params['max_int_time'] = 10
  params['model_converge_tol'] = 0.01

  params['TimeToControlAtt'] = 3 * np.log(10) * (np.sqrt(3) * params['sigma'] / np.pi + 1 / params['LambdaAtt'])
  params['TimeToControlDef'] = 3 * np.log(10) * (np.sqrt(3) * params['sigma'] / np.pi + 1 / params['LambdaDef'])

  return params

def generate_pitch_control(event_id, events, home, away, params, n_grid_cells_x=50):
  frame = events.loc[event_id]['Start Frame']
  team = events.loc[event_id].Team
  ball_pos = np.array([events.loc[event_id]['Start X'], events.loc[event_id]['Start Y']])

  n_grid_cells_y = int(n_grid_cells_x * 68 / 106)
  xgrid = np.linspace(-106/2.0, 68/2.0, n_grid_cells_x)
  ygrid = np.linspace(-68/2.0, 106/2.0, n_grid_cells_y)

  PPCFa = np.zeros(shape = (len(ygrid), len(xgrid)))
  PPCFd = np.zeros(shape = (len(ygrid), len(xgrid)))

  if team == 'Home':
    attacking_players = initialise_players(home.loc[frame], 'home', params)
    defending_players = initialise_players(away.loc[frame], 'away', params)
  elif team == 'Away':
    attacking_players = initialise_players(away.loc[frame], 'away', params)
    defending_players = initialise_players(home.loc[frame], 'home', params)

  for i in range(len(ygrid)):
    for j in range(len(xgrid)):
      target = np.array( [xgrid[j], ygrid[i]] )
      PPCFa[i, j], PPCFd[i, j] = calculate_pitch_control_target(target, attacking_players, defending_players, ball_pos, params)

  checksum = np.sum(PPCFa + PPCFd) / float(n_grid_cells_x * n_grid_cells_y)
  #assert 1 - checksum < params['model_converge_tol'], "Checksum Failed: %1.3f" % (1-checksum)
  return PPCFa, xgrid, ygrid

def initialise_players(team, teamname, params):
  player_ids = np.unique([c.split('_')[1] for c in team.keys() if c[:4] == teamname])
  team_players = []
  for p in player_ids:
    team_player = Player(p, team, teamname, params)
    if team_player.inframe:
      team_players.append(team_player)
  return team_players

class Player(object):

  def __init__(self, pid, team, teamname, params):
    self.id = pid
    self.teamname = teamname
    self.playername = "%s_%s_" % (teamname, pid)
    self.vmax = params['PlayerMaxSpd']
    self.reaction_time = params['PlayerReactTime']
    self.tti_sigma = params['sigma']
    self.get_position(team)
    self.get_velocity(team)
    self.PPCF = 0

  def get_position(self, team):
    self.position = np.array( team[self.playername + 'x'], team[self.playername + 'y'] )
    self.inframe = not np.any( np.isnan(self.position) )

  def get_velocity(self, team):
    self.velocity = np.array( [team[self.playername + 'vx'], team[self.playername + 'vy']] )
    if np.any( np.isnan(self.velocity) ):
      self.velocity = np.array([0., 0.])

  def simple_time_to_intercept(self, r_final):
    self.PPCF = 0.
    r_reaction = self.position + self.velocity * self.reaction_time
    self.time_to_intercept = self.reaction_time + np.linalg.norm(r_final - r_reaction) / self.vmax
    return self.time_to_intercept

  def probability_intercept_ball(self, T, s=0.45):
    f = 1 / (1. + np.exp(-np.pi / np.sqrt(3.0) / s * (T - self.time_to_intercept) ) )
    return f

def calculate_pitch_control_target(target_position, attacking_players, defending_players, ball_pos, params):
  if ball_pos is None or any(np.isnan(ball_pos)):
    ball_travel_time = 0.0
  else:
    ball_travel_time = np.linalg.norm(target_position - ball_pos) / params['BallSpd']

  tau_min_att = np.nanmin( [p.simple_time_to_intercept(target_position) for p in attacking_players] )
  tau_min_def = np.nanmin( [p.simple_time_to_intercept(target_position) for p in defending_players] )

  if tau_min_att - max(ball_travel_time, tau_min_def) >= params['TimeToControlDef']:
    return 0., 1.
  elif tau_min_def - max(ball_travel_time, tau_min_att) >= params['TimeToControlAtt']:
    return 1., 0.
  else:

    attacking_players = [p for p in attacking_players if p.time_to_intercept - tau_min_att < params['TimeToControlAtt']]
    defending_players = [p for p in defending_players if p.time_to_intercept - tau_min_def < params['TimeToControlDef']]

    dT_array = np.arange(ball_travel_time - params['int_dt'], ball_travel_time + params['max_int_time'], params['int_dt'])
    PPCFatt = np.zeros_like(dT_array)
    PPCFdef = np.zeros_like(dT_array)

    ptot = 0.0
    i = 1

    while 1 - ptot > params['model_converge_tol'] and i < dT_array.size:
      T = dT_array[i]
      for player in attacking_players:
        dPPCFdt = (1 - PPCFatt[i-1] - PPCFdef[i-1]) * player.probability_intercept_ball(T, s=params['sigma']) * params['LambdaAtt']
        assert dPPCFdt >= 0, 'Invalid probability'
        player.PPCF += dPPCFdt * params['int_dt']
        PPCFatt[i] += player.PPCF
      for player in defending_players:
        dPPCFdt = (1 - PPCFatt[i-1] - PPCFdef[i-1]) * player.probability_intercept_ball(T, s=params['sigma']) * params['LambdaDef']
        assert dPPCFdt >= 0, 'Invalid probability'
        player.PPCF += dPPCFdt * params['int_dt']
        PPCFdef[i] += player.PPCF
      ptot = PPCFdef[i] + PPCFatt[i]
      i += 1
    
    if i >= dT_array.size:
      print("Integration failed to converge: %1.3f - %1.3f - %1.3f" % (ptot, i, dT_array.size))
    return PPCFatt[i-1], PPCFdef[i-1]


