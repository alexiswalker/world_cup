import csv
import numpy as np
import keras

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
    title = 0
    runner_up = 0
    third = 0
    fourth = 0
    for row in positions_list:
        if row['title'] == team:
            title +=1
        if row['runner_up'] == team:
            runner_up +=1
        if row['third'] == team:
            third +=1
        if row['fourth'] == team:
            fourth +=1
    return title,  runner_up,  third, fourth

def matches_statistics(matches, team_name):
    team_matches = filter_data_field_equal_value(matches, 'home_team', team_name) +  filter_data_field_equal_value(matches, 'away_team', team_name)

    win = len(filter(lambda match : (match['home_team'] == team_name and match['home_score'] > match['away_score']) or (match['away_team'] == team_name and match['away_score'] > match['home_score']) , team_matches))
    lose = len(filter(lambda match : (match['home_team'] == team_name and match['home_score'] < match['away_score']) or (match['away_team'] == team_name and match['away_score'] < match['home_score']) , team_matches))
    tie = len(filter(lambda match : (match['home_team'] == team_name or match['away_team'] == team_name) and ( match['home_score'] == match['away_score']), team_matches))

    return win, lose, tie

def show_data(list_to_show, string_format, number_of_lines=5):
    for row in list_to_show[:number_of_lines]:
        print(string_format.format(**row))

def data_for_keras(matches, encode):
    x = []
    y = []

    neutral = {'TRUE':1, 'FALSE':0}

    for match in matches:
        x.append([int(match['year']), int(encode[match['home_team']]), int(encode[match['away_team']])])
        if int(match['home_score']) > int(match['away_score']):
            y.append(0)
        if int(match['home_score']) < int(match['away_score']):
            y.append(1)
        if int(match['home_score']) == int(match['away_score']):
            y.append(2)

    return np.array(x), keras.utils.to_categorical(np.array(y), num_classes=3)

def split_train_test(X, Y, percentage):
    limit = int(len(X)*percentage)

    X_train = X[:limit]
    X_test = X[limit+1:]
    y_train = Y[:limit]
    y_test = Y[limit+1:]

    return X_train, X_test, y_train, y_test


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
    #p = load_positions_data()
    #print positions(p, 'Germany')
    li = load_results_data()
    filter_data = filter_data_field_equal_value(li, 'tournament', 'FIFA World Cup')
    print matches_statistics(filter_data, 'Germany')
