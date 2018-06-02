import csv
import numpy as np

def load_data():
    match_list=[]
    with open('results.csv') as result_file:
        reader = csv.reader(result_file)
        next(reader) #data includes a first title line
        for row in reader:
            match_list.append({'date':row[0], 'year':row[0].split('-')[0],'home_team':row[1],'away_team':row[2],'home_score':row[3],'away_score':row[4],'tournament':row[5],'city':row[6],'country':row[7],'neutral':row[8]})

    return match_list

def different_teams_names(list_to_get_names):
    return list(set([row['home_team'] for row in list_to_get_names] + [row['away_team'] for row in list_to_get_names]))

def encode_teams_name(names):
    return dict((team_name, i) for i, team_name in enumerate(names))

def filter_data_field_equal_value(list_to_filter, field, value):
    return list(filter(lambda match : match[field] == value, list_to_filter))

def filter_data_field_not_equal_value(list_to_filter, field, value):
    return list(filter(lambda match : match[field] != value, list_to_filter))

def show_data(list_to_show, number_of_lines=5):
    for row in list_to_show[:number_of_lines]:
        print('{year} ({home_score}){home_team} ({away_score}){away_team} - {tournament}'.format(**row))

def data_for_keras(matches, encode):
    x = []
    y = []
    for match in matches:
        x.append([int(match['year']), int(encode[match['home_team']]), int(encode[match['away_team']]), int(bool(match['neutral'].lower()))])
        if match['home_score'] > match['away_score']:
            y.append([1,0,0])
        if match['home_score'] < match['away_score']:
            y.append([0,0,1])
        if match['home_score'] == match['away_score']:
            y.append([0,1,0])

    return np.array(x), np.array(y)

def split_train_test(X, Y, percentage):
    limit = int(len(X)*percentage)

    X_train = X[:limit]
    X_test = X[limit+1:]
    y_train = Y[:limit]
    y_test = Y[limit+1:]

    return X_train, X_test, y_train, y_test


if __name__ == '__main__':
    li = load_data()
    filter_data = filter_data_field_equal_value(li, 'tournament', 'FIFA World Cup')
    print(data_for_keras(filter_data, encode_teams_name(different_teams_names(filter_data))))
