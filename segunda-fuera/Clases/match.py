class match:
  def __init__(self, week, local, goal1, goal2, away):
    self.week = week
    self.local = local
    self.goal1 = goal1
    self.goal2 = goal2
    self.away = away

  def getResult(self):
    print("Week " + self.week + ", " + self.local + " " + self.goal1 + "-" + self.goal2 + " " + self.away)

  def getLocal(self):
    return self.local

  def getAway(self):
    return self.away

  def getLocalGoals(self):
    return self.goal1

  def getAwayGoals(self):
    return self.goal2