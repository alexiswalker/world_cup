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
        return home_team, prediction[0][0]
    else:
        return away_team, prediction[0][1]



if __name__ == '__main__':
    print predict_result('Iceland', 'Argentina', 2018)
    print predict_result('Argentina', 'Iceland', 2018)
