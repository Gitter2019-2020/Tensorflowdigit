import os
#ignore warning
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'


import  tensorflow as tf
import numpy as np
from tensorflow.keras import models

from training import train, preprocess

x = preprocess("./training/images/numero3.png")

model = train()
predictions = model.predict(x)
prediction = np.argmax(predictions)
print(prediction)
models.save_model(model, "./training/models/digits/1/")

model = models.load_model("./training/models/digits/1/")
predictions = model.predict(x)
prediction = np.argmax(predictions)
print(prediction)