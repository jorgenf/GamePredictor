from tensorflow import keras
import pandas as pd
import numpy as np


df = pd.read_csv("../data/combined.csv")
y = []
x = []
for i,s in df.iterrows():
    ss = s["home_score"] - s["away_score"]
    if ss > 0:
        y.append(0)
    elif ss < 0:
        y.append(1)
    else:
        y.append(2)
    h = s["home_lineup"]
    a = s["away_lineup"]
    h = h.strip("[")
    h = h.strip("]")
    h = h.split(", ")
    a = a.strip("[")
    a = a.strip("]")
    a = a.split(", ")
    xha = h + a
    xha = [float(x) for x in xha]
    x.append(xha)



y = np.asarray(y)
x = np.asarray(x)
print(type(x))

print(x.shape)
model = keras.models.Sequential()
model.add(keras.layers.Dense(50, input_shape=(x.shape[1],),activation="sigmoid"))
model.add(keras.layers.Dense(50, activation="sigmoid"))
model.add(keras.layers.Dense(50, activation="sigmoid"))
model.add(keras.layers.Dense(3, activation="softmax"))
print(model.summary())
model.compile(optimizer=keras.optimizers.Adam(learning_rate=0.001), loss=keras.losses.sparse_categorical_crossentropy, metrics="accuracy")
history = model.fit(x, y, batch_size=32, epochs=500, validation_split=0.2)

