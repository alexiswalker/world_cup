import numpy as np
from keras.models import Sequential
from keras.layers import Dense, Dropout
from util import show_data,load_data, filter_data_field_equal_value, filter_data_field_not_equal_value, different_teams_names, encode_teams_name, data_for_keras, split_train_test

#load data
#---------
matches = load_data()
countries_names = different_teams_names(matches)
encode = encode_teams_name(countries_names)

fifa_world_cup_matches = filter_data_field_equal_value(matches, 'tournament', 'FIFA World Cup')
fifa_world_cup_qualification_matches = filter_data_field_equal_value(matches, 'tournament', 'FIFA World Cup qualification')

#matches_2013 = filter_data_field_equal_value(matches, 'year', '2013')
matches_2014 = filter_data_field_equal_value(fifa_world_cup_matches + fifa_world_cup_qualification_matches, 'year', '2014')
matches_not_2014 = filter_data_field_not_equal_value(fifa_world_cup_matches + fifa_world_cup_qualification_matches, 'year', '2014')


#matches_2014 = filter_data_field_equal_value(fifa_world_cup_matches, 'year', '2014')
#matches_not_2014 = filter_data_field_not_equal_value(fifa_world_cup_matches, 'year', '2014')

X, Y = data_for_keras(fifa_world_cup_matches + fifa_world_cup_qualification_matches, encode)

X_train, X_test, y_train, y_test = split_train_test(X, Y, 0.2)
#X_train, y_train = data_for_keras(matches_not_2014, encode)
#X_cross_test, y_cross_test = data_for_keras(matches_2014, encode)
#X_test, y_test = data_for_keras(matches_2014, encode)


#create model
#------------
model = Sequential()

#neural network
#--------------
model.add(Dense(32, activation='relu', input_dim=3))
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

predictions = model.predict(np.array([[2018, int(encode['Argentina']), int(encode['Haiti'])]]))
print(predictions)
#score, acc  = model.evaluate(X_cross_test, y_cross_test)
#print('Test accuracy: %s: %.2f%%' % (model.metrics_names[1], scores[1]*100))
