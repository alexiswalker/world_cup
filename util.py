import csv

def load_data():
    match_list=[]
    with open('results.csv', newline='') as result_file:
        reader = csv.reader(result_file)
        next(reader) #data includes a first title line
        for row in reader:
            match_list.append({'date':row[0], 'year':row[0].split('-')[0],'home_team':row[1],'away_team':row[2],'home_score':row[3],'away_score':row[4],'tournament':row[5],'city':row[6],'country':row[7],'neutral':row[8]})

    return match_list

def different_teams_names(list_to_get_names):
    return list(set([row['home_team'] for row in list_to_get_names] + [row['away_team'] for row in list_to_get_names]))

def encode_teams_name(names):
    return dict((team_name, i) for i, team_name in enumerate(names))

def filter_data(list_to_filter, field, value):
    return list(filter(lambda match : match[field] == value, list_to_filter))

def show_data(list_to_show, number_of_lines=5):
    for row in list_to_show[:number_of_lines]:
        print('{year} ({home_score}){home_team} ({away_score}){away_team} - {tournament}'.format(**row))

if __name__ == '__main__':
    li = load_data()
    filter_data = filter_data(li, 'tournament', 'FIFA World Cup')
    print(encode_teams_name(different_teams_names(filter_data)))
    show_data(filter_data,10)
