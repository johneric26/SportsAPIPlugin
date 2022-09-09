# using MLB-StatsAPI Python wrapper for interface with MLB API
import statsapi

def get_team_id(name):
  # function for retrieving team id based on name input. Returns team id as integer
  team = statsapi.lookup_team(name)
  id = team[0].get('id')
  # print(id)
  # print(team)
  return id

# def game_match(team_id, date_in, time_in):
  # function for retrieving a team's game identifier based on a date input. Returns game primary key (gamePk) as integer