import numpy as np
from keras.models import Sequential
from keras.layers import Dense, Dropout
from util import *
from sklearn.model_selection import train_test_split
#load data
#---------
matches = load_results_data()

fifa_world_cup_matches = filter_data_field_equal_value(matches, 'tournament', 'FIFA World Cup')
fifa_world_cup_qualification_matches = filter_data_field_equal_value(matches, 'tournament', 'FIFA World Cup qualification')

#matches_2010 = filter_data_field_equal_value(matches, 'year', '2010')
#matches_2014 = filter_data_field_equal_value(fifa_world_cup_matches + fifa_world_cup_qualification_matches, 'year', '2014')
#matches_not_2014 = filter_data_field_not_equal_value(fifa_world_cup_matches + fifa_world_cup_qualification_matches, 'year', '2014')

filter_matches = fifa_world_cup_matches + fifa_world_cup_qualification_matches

#matches_2014 = filter_data_field_equal_value(filter_matches, 'year', '2014')
#matches_not_2014 = filter_data_field_not_equal_value(filter_matches, 'year', '2014')

X, y = data_for_keras(filter_matches)
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

#X_train, y_train = data_for_keras(matches_not_2014)
#X_test, y_test = data_for_keras(matches_2014)


#X_train, y_train = data_for_keras(matches_not_2014, encode)
#X_cross_test, y_cross_test = data_for_keras(matches_2014, encode)
#X_test, y_test = data_for_keras(matches_2014, encode)

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
