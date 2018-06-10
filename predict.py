from statistics import get_statistics, get_scores, get_year_statistics
import numpy as np
import keras as k

model = k.models.load_model('world_cup_model.h5')

def predict_result(home_team, away_team, year):
    X_predict = np.array([
                                [1] +
                                get_statistics(home_team) + get_scores(home_team) + get_year_statistics(str(year),home_team) + get_year_statistics(str(year-1),home_team) +
                                get_statistics(away_team) + get_scores(away_team) + get_year_statistics(str(year),away_team) + get_year_statistics(str(year-1),away_team)
                        ])

    prediction = model.predict(X_predict)

    if (prediction[0][0] > prediction[0][1]):
        return home_team + ': ' + str(prediction[0][0])
    else:
        return away_team + ': ' + str(prediction[0][1])



if __name__ == '__main__':
    world_cup_matches_russia_2018 = [
            ('Russia', 'Saudi Arabia'),
            ('Egypt', 'Uruguay'),
            ('Morocco', 'Iran'),
            ('Portugal', 'Spain'),
            ('France', 'Australia'),
            ('Argentina', 'Iceland'),
            ('Peru', 'Denmark'),
            ('Croatia', 'Nigeria'),
            ('Costa Rica', 'Serbia'),
            ('Germany', 'Mexico'),
            ('Brazil', 'Switzerland'),
            ('Sweden', 'Korea Republic'),
            ('Belgium', 'Panama'),
            ('Tunisia', 'England'),
            ('Colombia', 'Japan'),
            ('Poland', 'Senegal'),
            ('Russia', 'Egypt'),
            ('Portugal', 'Morocco'),
            ('Uruguay', 'Saudi Arabia'),
            ('Iran', 'Spain'),
            ('Denmark', 'Australia'),
            ('France', 'Peru'),
            ('Argentina', 'Croatia'),
            ('Brazil', 'Costa Rica'),
            ('Nigeria', 'Iceland'),
            ('Serbia', 'Switzerland'),
            ('Belgium', 'Tunisia'),
            ('Korea Republic', 'Mexico'),
            ('Germany', 'Sweden'),
            ('England', 'Panama'),
            ('Japan', 'Senegal'),
            ('Poland', 'Colombia'),
            ('Saudi Arabia', 'Egypt'),
            ('Uruguay', 'Russia'),
            ('Iran', 'Portugal'),
            ('Spain', 'Morocco'),
            ('Australia', 'Peru'),
            ('Denmark', 'France'),
            ('Nigeria', 'Argentina'),
            ('Iceland', 'Croatia'),
            ('Mexico', 'Sweden'),
            ('Korea Republic', 'Germany'),
            ('Switzerland', 'Costa Rica'),
            ('Serbia', 'Brazil'),
            ('Senegal', 'Colombia'),
            ('Japan', 'Poland'),
            ('England', 'Belgium'),
            ('Panama', 'Tunisia')
        ]

    file = open('predictions.txt','w')

    for team1, team2 in world_cup_matches_russia_2018:
        file.write(team1 + ' vs ' + team2 + '\n')
        file.write(predict_result(team1, team2, 2018) + '\n')
        file.write(predict_result(team2, team1, 2018) + '\n')
        file.write('-----------------------\n')

    file.close()

'''
Egypt
Morocco
Nigeria
Senegal
Tunisia
Saudi Arabia
Australia
Japan
Korea Republic,
Iran
Germany
Belgium
Croatia
Denmark
Spain
France
England
Iceland
Poland
Portugal
Russia
Serbia
Sweden
Switzerland
Costa Rica
Mexico
Panama
Argentina
Brazil
Colombia
Peru
Uruguay
'''
