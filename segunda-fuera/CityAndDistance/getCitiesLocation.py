import requests
import urllib
import sys
import geopy.distance

def getDistance(team1, team2):
  api_url = "http://www.mapquestapi.com/directions/v2/route?"
  key = "XPGaPHF0F6kqWSAJAeJx2LIuDcGyG7M3"

  coord_distance = {
    "coord1": {
      "lat": 0,
      "lon": 0
    },
    "coord2": {
      "lat": 0,
      "lon": 0
    },
    "distance": 0
  }

  url = api_url + urllib.parse.urlencode({"key": key, "from": team1.city, "to": team2.city})
  print(url)
  json_data = requests.get(url).json()
  result = list(json_data.keys())[0]
  print(result)
  while True:
    if result == 'fault':
      print("Repeat")
      json_data = requests.get(url).json()
    elif result == 'route':
      break
      

  
  coord_distance["coord1"]["lat"] = json_data["route"]["locations"][0]["latLng"]["lat"]
  coord_distance["coord1"]["lon"] = json_data["route"]["locations"][0]["latLng"]["lng"]

  coord_distance["coord2"]["lat"] = json_data["route"]["locations"][1]["latLng"]["lat"]
  coord_distance["coord2"]["lon"] = json_data["route"]["locations"][1]["latLng"]["lng"]

  coord1 = (float(coord_distance["coord1"]["lat"]), float(coord_distance["coord1"]["lon"]))
  coord2 = (float(coord_distance["coord2"]["lat"]), float(coord_distance["coord2"]["lon"]))

  coord_distance["distance"] = round(geopy.distance.geodesic(coord1, coord2).km, 2)

  print(coord_distance["distance"])

  if json_data["info"]["statuscode"] == 402:
    print("Fail: Error in " + team1.ciudad + " or " + team2.ciudad)
    sys.exit()

  return coord_distance
