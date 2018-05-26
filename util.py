import csv

def load_data():
    match_list=[]
    with open('results.csv', newline='') as result_file:
        reader = csv.reader(result_file)
        next(reader) #data includes a first title line
        for row in reader:
            match_list.append({'date':row[0],'home_team':row[1],'away_team':row[2],'home_score':row[3],'away_score':row[4],'tournament':row[5],'city':row[6],'country':row[7],'neutral':row[8]})

    return match_list

def filter_data(list_to_filter, field, value):
    return list(filter(lambda match : match[field] == value, list_to_filter))

if __name__ == '__main__':
    li = load_data()
    argentina = filter_data(li, 'tournament', 'FIFA World Cup')

    for m in argentina:
        print (m)

    print (len(argentina))
