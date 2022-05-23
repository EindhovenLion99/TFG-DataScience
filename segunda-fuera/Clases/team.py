from Clases.match import match


class team:
  def __init__(self, team_name, city_name):
    self.name = team_name
    self.matches = []
    self.stadium = ""
    self.city = city_name
    self.statistycs = {
      'statsLocal': {
        "wins": 0,
        "draws": 0,
        "loses": 0
      },
      'statsAway': {
        "wins": 0,
        "draws": 0,
        "loses": 0
      }
    }

  def setStadium(self, stadium_name):
    self.stadium = stadium_name

  def getName(self):
    return self.name

  def getStadium(self):
    return self.stadium

  def getMatches(self):
    return self.matches

  def setMatch(self, match):
    self.matches.append(match)
    if (match.getLocal() == self.name):
      if match.getLocalGoals() > match.getAwayGoals():
        self.statistycs['statsLocal']["wins"] += 1
      elif match.getLocalGoals() == match.getAwayGoals():
        self.statistycs['statsLocal']["draws"] += 1
      else:
        self.statistycs['statsLocal']["loses"] += 1
    else:
      if match.getLocalGoals() < match.getAwayGoals():
        self.statistycs['statsAway']["wins"] += 1
      elif match.getLocalGoals() == match.getAwayGoals():
        self.statistycs['statsAway']["draws"] += 1
      else:
        self.statistycs['statsAway']["loses"] += 1

  def getNumMatches(self):
    return len(self.matches)

  def getStatistycs(self):
    print(self.statistycs)

