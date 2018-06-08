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

def encode_teams_name(names):
    return dict((team_name, i) for i, team_name in enumerate(names))

def filter_data_field_equal_value(list_to_filter, field, value):
    return list(filter(lambda match : match[field] == value, list_to_filter))

def filter_data_field_not_equal_value(list_to_filter, field, value):
    return list(filter(lambda match : match[field] != value, list_to_filter))

def positions(positions_list, team):
    title =  len(filter(lambda world_cup : world_cup['title'] == team, positions_list))
    runner_up = len(filter(lambda world_cup : world_cup['runner_up'] == team, positions_list))
    third = len(filter(lambda world_cup : world_cup['third'] == team, positions_list))
    fourth = len(filter(lambda world_cup : world_cup['fourth'] == team, positions_list))

    return [title*8 + runner_up*4 + third*2 + fourth]

def matches_statistics(matches, team_name):
    team_matches = filter_data_field_equal_value(matches, 'home_team', team_name) +  filter_data_field_equal_value(matches, 'away_team', team_name)

    win = len(filter(lambda match : (match['home_team'] == team_name and match['home_score'] > match['away_score']) or (match['away_team'] == team_name and match['away_score'] > match['home_score']) , team_matches))
    lose = len(filter(lambda match : (match['home_team'] == team_name and match['home_score'] < match['away_score']) or (match['away_team'] == team_name and match['away_score'] < match['home_score']) , team_matches))
    tie = len(filter(lambda match : (match['home_team'] == team_name or match['away_team'] == team_name) and ( match['home_score'] == match['away_score']), team_matches))
    #total = len(filter(lambda match : match['home_team'] == team_name or match['away_team'] == team_name, matches))

    return [win*1.0/(win+lose+tie)]

def show_data(list_to_show, string_format, number_of_lines=5):
    for row in list_to_show[:number_of_lines]:
        print(string_format.format(**row))

def data_for_keras(matches):

    teams = different_teams_names(matches)
    countries_positions = load_positions_data()
    features = dict((team, matches_statistics(matches, team) + positions(countries_positions, team)) for team in teams)

    X = []
    y = []

    for match in matches:
        if match['neutral'] == 'TRUE':
            neutral = 1
        else:
            neutral = 0

        X.append([neutral] + [int(match['year'])] + features[match['home_team']] + features[match['away_team']])

        if int(match['home_score']) > int(match['away_score']):
            y.append(0)
        if int(match['home_score']) < int(match['away_score']):
            y.append(1)
        if int(match['home_score']) == int(match['away_score']):
            y.append(2)

    X, y = np.array(X), keras.utils.to_categorical(np.array(y), num_classes=3)

    return X, y



if __name__ == '__main__':
    '''
    li = load_results_data()
    filter_data = filter_data_field_equal_value(li, 'tournament', 'FIFA World Cup')
    filter_data_arq_h = filter_data_field_equal_value(filter_data, 'home_team', 'France')
    filter_data_arq_a = filter_data_field_equal_value(filter_data, 'away_team', 'France')
    filter_data = filter_data_field_equal_value(filter_data_arq_h+filter_data_arq_a, 'year', '2006')
    show_data(filter_data,STRING_FORMAT_MATCHES, 60)

    show_data(p, STRING_FORMAT_POSITIONS, 50)
    print(len(filter_data))
    #print(data_for_keras(filter_data, encode_teams_name(different_teams_names(filter_data))))
    '''
    p = load_positions_data()

    li = load_results_data()
    filter_data = filter_data_field_equal_value(li, 'tournament', 'FIFA World Cup')

    print matches_statistics(filter_data, 'Germany')
