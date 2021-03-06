
from keras.models import Sequential
from keras.layers import Dense, Dropout, Activation
from sklearn.model_selection import train_test_split
from keras.optimizers import RMSprop, SGD
from statistics import filter_matches, get_scores, get_statistics,get_year_statistics
import numpy as np
import keras
#statistics for keras
X = []
y = []

for match in filter_matches:
    if match['neutral'] == 'TRUE':
        X.append(
                    [1] +
                    #[int(match['year'])] +
                    get_statistics(match['home_team']) +
                    get_scores(match['home_team']) +
                    get_year_statistics(str(int(match['year'])), match['home_team']) +
                    get_year_statistics(str(int(match['year'])-1), match['home_team']) +
                    get_statistics(match['away_team']) +
                    get_scores(match['away_team']) +
                    get_year_statistics(str(int(match['year'])), match['away_team'])+
                    get_year_statistics(str(int(match['year'])-1), match['away_team'])
                )

        if int(match['home_score']) > int(match['away_score']):
            y.append(0)
        if int(match['home_score']) < int(match['away_score']):
            y.append(1)

        X.append(
                    [1] +
                    #[int(match['year'])] +
                    get_statistics(match['away_team']) +
                    get_scores(match['away_team']) +
                    get_year_statistics(str(int(match['year'])), match['away_team']) +
                    get_year_statistics(str(int(match['year'])-1), match['away_team']) +
                    get_statistics(match['home_score']) +
                    get_scores(match['home_score']) +
                    get_year_statistics(str(int(match['year'])), match['home_score'])+
                    get_year_statistics(str(int(match['year'])-1), match['home_score'])
                )

        if int(match['away_score']) > int(match['home_score']):
            y.append(0)
        if int(match['away_score']) < int(match['home_score']):
            y.append(1)

    else:
        X.append(
                    [0] +
                    #[int(match['year'])] +
                    get_statistics(match['home_team']) +
                    get_scores(match['home_team']) +
                    get_year_statistics(str(int(match['year'])), match['home_team']) +
                    get_year_statistics(str(int(match['year'])-1), match['home_team']) +
                    get_statistics(match['away_team']) +
                    get_scores(match['away_team']) +
                    get_year_statistics(str(int(match['year'])), match['away_team'])+
                    get_year_statistics(str(int(match['year'])-1), match['away_team'])
                )

        if int(match['home_score']) > int(match['away_score']):
            y.append(0)
        if int(match['home_score']) < int(match['away_score']):
            y.append(1)

X, y = np.array(X), keras.utils.to_categorical(np.array(y), num_classes=2)


#split
#-----
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

#create model
#------------
model = Sequential()

#neural network
#--------------
model.add(Dense(128, input_dim=21, init='uniform'))
model.add(Activation('tanh'))
model.add(Dropout(0.5))
model.add(Dense(128, init='uniform'))
model.add(Activation('tanh'))
model.add(Dropout(0.5))
model.add(Dense(128, init='uniform'))
model.add(Activation('tanh'))
model.add(Dropout(0.5))
model.add(Dense(2, init='uniform'))
model.add(Activation('softmax'))

#optimizer = SGD(lr=0.1, decay=1e-6, momentum=0.9, nesterov=True)
optimizer = RMSprop(lr=0.001, rho=0.9, epsilon=None, decay=0.0)
#optimizer = keras.optimizers.Adagrad(lr=0.01, epsilon=None, decay=0.0)
#optimizer = keras.optimizers.Adadelta(lr=1.0, rho=0.95, epsilon=None, decay=0.0)
#optimizer = keras.optimizers.Adam(lr=0.001, beta_1=0.9, beta_2=0.999, epsilon=None, decay=0.0, amsgrad=False)
#optimizer = keras.optimizers.Adamax(lr=0.002, beta_1=0.9, beta_2=0.999, epsilon=None, decay=0.0)
#optimizer = keras.optimizers.Nadam(lr=0.002, beta_1=0.9, beta_2=0.999, epsilon=None, schedule_decay=0.004)

model.compile(loss = 'categorical_crossentropy', optimizer = optimizer, metrics=['accuracy'])

model.fit(X_train, y_train, epochs=20, batch_size=128)
#
model_scores = model.evaluate(X_test, y_test)
print model_scores
print('Test accuracy: %s: %.2f%%' % (model.metrics_names[1], model_scores[1]*100))

model.save('world_cup_model.h5')  # creates a HDF5 file 'my_model.h5'
del model  # deletes the existing model




'''
X_predict = np.array([
                            [1] +
                            get_statistics('Argentina') + get_scores('Argentina') + get_year_statistics('2018','Argentina') + get_year_statistics('2017','Argentina') +
                            get_statistics('Paraguay') + get_scores('Paraguay') + get_year_statistics('2018','Paraguay') + get_year_statistics('2017','Paraguay')
                    ])

print model.predict(X_predict)
'''
#score, acc  = model.evaluate(X_cross_test, y_cross_test)
#print('Test accuracy: %s: %.2f%%' % (model.metrics_names[1], scores[1]*100))
