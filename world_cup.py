from keras.models import Sequential
from keras.layers import Dense, Dropout
from util import load_data, filter_data, different_teams_names, encode_teams_name, data_for_keras

#load data
#---------
matches = load_data()
fifa_world_cup_matches = filter_data(matches, 'tournament', 'FIFA World Cup')
countries_names = different_teams_names(fifa_world_cup_matches)
encode = encode_teams_name(countries_names)
X, Y = data_for_keras(fifa_world_cup_matches, encode)

percentage = 0.2
limit = int(len(X)*percentage)


X_train = X[:limit]
X_test = X[limit+1:]
y_train = Y[:limit]
y_test = Y[limit+1:]


#create model
#------------
model = Sequential()

#neural network
#--------------
model.add(Dense(units=64, activation='relu', input_dim=3))
model.add(Dropout(0.5))
model.add(Dense(units=64, activation='relu'))
model.add(Dropout(0.5))
model.add(Dense(units=64, activation='relu'))
model.add(Dropout(0.5))
model.add(Dense(units=64, activation='relu'))
model.add(Dropout(0.5))
model.add(Dense(units=3, activation='sigmoid'))

model.compile(loss='categorical_crossentropy',
              optimizer='sgd',
              metrics=['accuracy'])

model.fit(X_train, y_train, epochs=5, batch_size=32)

score, acc  = model.evaluate(X_test, y_test, batch_size=128)
print('Test score:', score)
print('Test accuracy:', acc)
