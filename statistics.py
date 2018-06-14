import numpy as np
from util import *

#functions
#---------
positions_list = load_positions_data()
def positions(team):
    title =  len(filter(lambda world_cup : world_cup['title'] == team, positions_list))
    runner_up = len(filter(lambda world_cup : world_cup['runner_up'] == team, positions_list))
    third = len(filter(lambda world_cup : world_cup['third'] == team, positions_list))
    fourth = len(filter(lambda world_cup : world_cup['fourth'] == team, positions_list))

    return [title*8, runner_up*4, third*2, fourth]

def matches_statistics(matches, team_name):
    team_matches = list(
                        filter(lambda match :
                                    match['home_team'] == team_name
                                    or
                                    match['away_team'] == team_name,
                                matches))

    win = len(filter(lambda match : (match['home_team'] == team_name and match['home_score'] > match['away_score']) or (match['away_team'] == team_name and match['away_score'] > match['home_score']) , team_matches))
    lose = len(filter(lambda match : (match['home_team'] == team_name and match['home_score'] < match['away_score']) or (match['away_team'] == team_name and match['away_score'] < match['home_score']) , team_matches))
    tie = len(filter(lambda match : (match['home_team'] == team_name or match['away_team'] == team_name) and ( match['home_score'] == match['away_score']), team_matches))

    total = len(matches)

    return [win*1.0/total, lose*1.0/total]

#load data
#---------
matches = load_results_data()

#data for training and test
#--------------------------
filter_matches = list(
                        filter(lambda match :
                                    (match['tournament'] == 'FIFA World Cup'
                                    or
                                    match['tournament'] == 'FIFA World Cup qualification')
                                    and
                                    match['home_score'] != match['away_score']
                                ,matches))


#statistics
#----------
different_teams_names = different_teams_names(filter_matches)
different_years = different_years(filter_matches)

_year_statistics = {}
for year in different_years:
    year_matches = list(filter(lambda match : match['year'] == year, filter_matches))
    _year_statistics[year] = {}
    for team in different_teams_names:
        _year_statistics[year][team] = matches_statistics(year_matches, team)

_statistics = dict((team, matches_statistics(filter_matches, team)) for team in different_teams_names)
_scores = dict((team, positions(team)) for team in different_teams_names)

#api
#---

def get_statistics(team):
    if team in _statistics:
        return _statistics[team]
    else:
        return len(_statistics[_statistics.keys()[0]])*[0]

def get_year_statistics(year, team):
    if year in _year_statistics:
        if team in _year_statistics[year]:
            return _year_statistics[year][team]

    first_key = _year_statistics.keys()[0]
    second_key = _year_statistics[first_key].keys()[0]
    return len(_year_statistics[first_key][second_key])*[0]

def get_scores(team):
    if team in _scores:
        return _scores[team]
    else:
        return len(_scores[_scores.keys()[0]])*[0]

if __name__ == '__main__':
    print get_year_statistics('20145','Argentina')
