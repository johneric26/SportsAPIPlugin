import requests
import json
import statistics

# define base url for all functions
baseurl = "https://api.the-odds-api.com"

def get_sports(apikey):
  # returns all sports and reads JSON data to load to dictionary named data
  r = requests.get(baseurl+"/v4/sports?apiKey="+apikey)
  data = json.loads(r.text)
  return data

def get_odds(apikey, sportkey, region, market="h2h", books=""):
  # returns active odds for given sport & market, with optional arguments for providing unique markets and books
  if books=="":
    requesturl = baseurl+"/v4/sports/"+sportkey+"/odds/?apiKey="+apikey+"&regions="+region+"&markets="+market
    r = requests.get(requesturl)
  else:
    requesturl = baseurl+"/v4/sports/"+sportkey+"/odds/?apiKey="+apikey+"&markets="+market
    params = {'bookmakers': books}
    r = requests.get(requesturl, params)
  data = json.loads(r.text)
  return data

def implied_odds(odds_data):
  # calculate average (and other stats) implied odds for provided odds data
  # assumes odds_data provided in standard json format from odds api, for single bet market type (e.g. h2h)
  ostats = []
  for i in odds_data:
    marketstats = []
    hometeam = i['home_team']
    awayteam = i['away_team']
    for m in {"h2h", "spreads", "totals"}:
      odds1 = []
      odds2 = []
      for j in i['bookmakers']:
        count = 0
        marketfilter = list(filter(lambda k: k['key'] in m, j['markets']))
        if len(marketfilter) > 0:
          while count <= 1:
            target = marketfilter[0]['outcomes'][count]
            if m == "h2h" or m == "spreads":
              if target['name'] == awayteam:
                odds1.append(target['price'])
              elif target['name'] == hometeam:
                odds2.append(target['price'])
              count = count + 1
            elif m == "totals":
              if target['name'] == "Over":
                odds1.append(target['price'])
              elif target['name'] == "Under":
                odds2.append(target['price'])
              count = count + 1
            else:
              print("error in odds statistics processing, unidentified market type")
      # done looping through bookmakers for given market, calculate summary statistics
      if len(odds1) > 0 and len(odds2) > 0:
        avg1 = statistics.mean(odds1)
        avg2 = statistics.mean(odds2)
        impliedodds1 = 1/avg1
        impliedodds2 = 1/avg2
        # create market stats list. Format for implied odds will be: away-home or over-under
        marketstats.append({'key': m, 'impliedodds1': impliedodds1, 'impliedodds2': impliedodds2})
    ostats.append(
      {'id': str(i["id"]), 'hometeam': hometeam,'awayteam': awayteam, 'marketstats': marketstats})
  return ostats

    
# def expectedvalues(odds_data, odds_stats):
#   # compares a given set of odds data to find positive expected value bets
#   for i in odds_data:
#     # commented out for later implementation in non-h2h markets
#     # for m in {"h2h", "spreads", "totals"}
#     for m in {"h2h"}:
#       gamefilter = list(filter(lambda id: id["id"] in i["id"], odds_stats))
#       # will need to be updated for new markets (some combo of 1st, second implied odds)
#       homeimpliedodds = gamefilter[0]['homeimpliedodds']
#       awayimpliedodds = gamefilter[0]['awayimpliedodds']
#       for b in i['bookmakers']:
#         for n in b['markets']:
#           if n['key'] == m.str():
#             j = 1
#             count = 0
#             while count <=1:
#               payout1 = n['outcomes'][count]['price']
              
#               count = count + 1