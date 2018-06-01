from keras.models import Sequential
from keras.layers import Dense
model = Sequential()


model.add(Dense(units=64, activation='relu', input_dim=3))
model.add(Dense(units=3, activation='sigmoid'))

model.compile(loss='categorical_crossentropy',
              optimizer='sgd',
              metrics=['accuracy'])


'''
model.fit(x_train, y_train, epochs=5, batch_size=32)

loss_and_metrics = model.evaluate(x_test, y_test, batch_size=128)

print (loss_and_metrics)
'''
