import numpy as np
from keras.models import Sequential
from keras.layers import Dense, Dropout
from util import *
#load data
#---------
matches = load_results_data()
countries_positions = load_positions_data()

fifa_world_cup_matches = filter_data_field_equal_value(matches, 'tournament', 'FIFA World Cup')
fifa_world_cup_qualification_matches = filter_data_field_equal_value(matches, 'tournament', 'FIFA World Cup qualification')


#matches_2010 = filter_data_field_equal_value(matches, 'year', '2010')
#matches_2014 = filter_data_field_equal_value(fifa_world_cup_matches + fifa_world_cup_qualification_matches, 'year', '2014')
#matches_not_2014 = filter_data_field_not_equal_value(fifa_world_cup_matches + fifa_world_cup_qualification_matches, 'year', '2014')

filter_matches = fifa_world_cup_matches + fifa_world_cup_qualification_matches

teams = different_teams_names(filter_matches)

features = dict((team, np.array(matches_statistics(filter_matches, team) + positions(countries_positions, team))) for team in teams)

X = []
y = []

for match in filter_matches:
    X.append(np.append(features[match['home_team']], features[match['away_team']]))
    if int(match['home_score']) > int(match['away_score']):
        y.append(0)
    if int(match['home_score']) < int(match['away_score']):
        y.append(1)
    if int(match['home_score']) == int(match['away_score']):
        y.append(2)

X, y = np.array(X), keras.utils.to_categorical(np.array(y), num_classes=3)

X_train, X_test, y_train, y_test = split_train_test(X, y, 0.2)
#X_train, y_train = data_for_keras(matches_not_2014, encode)
#X_cross_test, y_cross_test = data_for_keras(matches_2014, encode)
#X_test, y_test = data_for_keras(matches_2014, encode)

#create model
#------------
model = Sequential()

#neural network
#--------------
model.add(Dense(32, activation='relu', input_dim=14))
model.add(Dropout(0.5))
model.add(Dense(32, activation='relu'))
model.add(Dropout(0.5))
model.add(Dense(32, activation='relu'))
model.add(Dropout(0.5))
model.add(Dense(3, activation='softmax'))
model.compile(optimizer='rmsprop',
              loss='categorical_crossentropy',
              metrics=['accuracy'])

model.fit(X_train, y_train, epochs=10, batch_size=128)

scores = model.evaluate(X_test, y_test, batch_size=128)
print('Test accuracy: %s: %.2f%%' % (model.metrics_names[1], scores[1]*100))


#score, acc  = model.evaluate(X_cross_test, y_cross_test)
#print('Test accuracy: %s: %.2f%%' % (model.metrics_names[1], scores[1]*100))
