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



