import tensorflow as tf
from tensorflow import keras
import numpy as np
import get_xy_for_network
from sklearn.metrics import r2_score


X = np.array(get_xy_for_network.X)
Y = np.array(get_xy_for_network.Y)

# model = keras.models.load_model('model.h5')

model = keras.Sequential([
    keras.layers.Dense(8, input_dim=8, activation='relu'),
    keras.layers.Dense(4, activation='relu'),
    keras.layers.Dense(1, activation='sigmoid'),
])

model.compile(optimizer='adam',
              loss='mean_squared_error',
              metrics=['accuracy'])

model.fit(X, Y, epochs=1000, batch_size=10)

test_loss, test_acc = model.evaluate(X, Y)

model.save('model.h5')

prediction = model.predict(X)

print(r2_score(Y, prediction))
