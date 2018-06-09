import numpy as np
from keras.models import Sequential
from keras.layers import Dense, Dropout
from util import *
from sklearn.model_selection import train_test_split
#load data
#---------
matches = load_results_data()
countries_positions = load_positions_data()

filter_matches = list(
                        filter(lambda match :
                                    match['tournament'] == 'FIFA World Cup'
                                    or
                                    match['tournament'] == 'FIFA World Cup qualification'
                                ,matches))

different_teams_names = different_teams_names(filter_matches)



statistics = dict((team, matches_statistics(filter_matches, team)) for team in different_teams_names)
scores = dict((team, positions(countries_positions, team)) for team in different_teams_names)


X = []
y = []

for match in filter_matches:
    if match['neutral'] == 'TRUE':
        neutral = 1
    else:
        neutral = 0

    X.append(
                [neutral] +
                [int(match['year'])] +
                statistics[match['home_team']] +
                scores[match['home_team']] +
                statistics[match['away_team']] +
                scores[match['away_team']]
            )

    if int(match['home_score']) > int(match['away_score']):
        y.append(0)
    if int(match['home_score']) < int(match['away_score']):
        y.append(1)
    if int(match['home_score']) == int(match['away_score']):
        y.append(2)

X, y = np.array(X), keras.utils.to_categorical(np.array(y), num_classes=3)


X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)



#create model
#------------
model = Sequential()

#neural network
#--------------
model.add(Dense(64, activation='relu', input_dim=6))
model.add(Dropout(0.5))
model.add(Dense(64, activation='relu'))
model.add(Dropout(0.5))
model.add(Dense(64, activation='relu'))
model.add(Dropout(0.5))
model.add(Dense(64, activation='relu'))
model.add(Dropout(0.5))
model.add(Dense(64, activation='relu'))
model.add(Dropout(0.5))
model.add(Dense(3, activation='softmax'))

#optimizer = keras.optimizers.SGD(lr=0.01, momentum=0.0, decay=0.0, nesterov=False)
optimizer = keras.optimizers.RMSprop(lr=0.001, rho=0.9, epsilon=None, decay=0.0)
#optimizer = keras.optimizers.Adagrad(lr=0.01, epsilon=None, decay=0.0)
#optimizer = keras.optimizers.Adadelta(lr=1.0, rho=0.95, epsilon=None, decay=0.0)
#optimizer = keras.optimizers.Adam(lr=0.001, beta_1=0.9, beta_2=0.999, epsilon=None, decay=0.0, amsgrad=False)
#optimizer = keras.optimizers.Adamax(lr=0.002, beta_1=0.9, beta_2=0.999, epsilon=None, decay=0.0)
#optimizer = keras.optimizers.Nadam(lr=0.002, beta_1=0.9, beta_2=0.999, epsilon=None, schedule_decay=0.004)

model.compile(loss='categorical_crossentropy',
              optimizer = optimizer,
              metrics=['accuracy'])

model.fit(X_train, y_train)
#
scores = model.evaluate(X_test, y_test)
print('Test accuracy: %s: %.2f%%' % (model.metrics_names[1], scores[1]*100))


#score, acc  = model.evaluate(X_cross_test, y_cross_test)
#print('Test accuracy: %s: %.2f%%' % (model.metrics_names[1], scores[1]*100))
