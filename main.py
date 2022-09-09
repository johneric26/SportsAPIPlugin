#import MLBStats
#import statsapi
#team_id = MLBStats.get_team_id('Cubs')
#statsapi next_game function by default returns integer value for gamePk
#game = statsapi.next_game(team_id)
#print(game)

import OddsProcess
import ast
import json

apikey = "a3b12a08bee9f664e00b3b8eefead5dd"
baseurl = "https://api.the-odds-api.com"

allsports = OddsProcess.get_sports(apikey)

groups = {"American Football", "Basketball"}

output = list(filter(lambda d: d["group"] in groups, allsports))
# print(output)

NFL = list(filter(lambda k: k["title"] in "NFL", output))[0]
sportkey = NFL["key"]
books = "fanduel,barstool,betrivers,draftkings,pointsbetus,betmgm"

# 9/7 -- commented out to not hit against api quota while evaluating the books used
# odds = OddsProcess.get_odds(apikey, sportkey, "us", "h2h", books)
# f = open("file.txt", "w+")
# f.write(str(odds))
# print(odds)

# 9/7 -- building odds comparsion for positive EV bets with 
with open("file.txt") as f:
  odds = ast.literal_eval(f.read())
json_formatted = json.dumps(odds, indent=1)

stats = OddsProcess.implied_odds(odds)
json_formatted = json.dumps(stats, indent=1)
print(json_formatted)

# evs = OddsProcess.expectedvalues(odds, stats)

# 9/ 7 -- finding the sports books covered by Odds API
# opening string written out from current nfl odds
# with open("file.txt") as f:
  # odds = ast.literal_eval(f.read())

# finding bookmakers provided
# books = []
# j = 0
# for i in odds:
  # books.append(i["bookmakers"])
  # j = j + 1
# print(books)