import csv
import numpy as np
import keras
from sklearn.preprocessing import MinMaxScaler

STRING_FORMAT_MATCHES = '{date} ({home_score}){home_team} ({away_score}){away_team} - {tournament}'
STRING_FORMAT_POSITIONS = '{year} {title} {runner_up} {third} {fourth}'

def load_results_data():
    match_list=[]
    with open('results.csv') as result_file:
        reader = csv.reader(result_file)
        next(reader) #data includes a first title line
        for row in reader:
            match_list.append({'date':row[0], 'year':row[0].split('-')[0],'home_team':row[1],'away_team':row[2],'home_score':row[3],'away_score':row[4],'tournament':row[5],'city':row[6],'country':row[7],'neutral':row[8]})

    return match_list

def load_positions_data():
    world_cups_list=[]
    with open('positions.csv') as result_file:
        reader = csv.reader(result_file)
        next(reader) #data includes a first title line
        for row in reader:
            world_cups_list.append({'year':row[0], 'title':row[1],'runner_up':row[2],'third':row[3],'fourth':row[4]})

    return world_cups_list

def different_teams_names(list_to_get_names):
    return list(set([row['home_team'] for row in list_to_get_names] + [row['away_team'] for row in list_to_get_names]))

def positions(positions_list, team):
    title =  len(filter(lambda world_cup : world_cup['title'] == team, positions_list))
    runner_up = len(filter(lambda world_cup : world_cup['runner_up'] == team, positions_list))
    third = len(filter(lambda world_cup : world_cup['third'] == team, positions_list))
    fourth = len(filter(lambda world_cup : world_cup['fourth'] == team, positions_list))

    return [title*8 + runner_up*4 + third*2 + fourth]

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
    #total = len(filter(lambda match : match['home_team'] == team_name or match['away_team'] == team_name, matches))

    return [win*1.0/(win+lose+tie)]

def show_data(list_to_show, string_format, number_of_lines=5):
    for row in list_to_show[:number_of_lines]:
        print(string_format.format(**row))


if __name__ == '__main__':
    pass
