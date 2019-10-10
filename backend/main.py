import os
#ignore warning
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'


import  tensorflow as tf
from tensorflow.keras import models
import numpy as np

from training import load_data, display_images, normalize_data, create_model, evaluate_model, preprocess


x_train, y_train, x_test, y_test = load_data()
# display_images(x_train, 5, 5)
# display_images(x_test, 3, 3)

x_train = normalize_data(x_train)
#display_images(x_train[0:25,:,:,0]*255, y_train[0:25], 5, 5)
x_test = normalize_data(x_test)
#display_images(x_test[0:4,:,:,0]*255, y_test[0:4], 2, 2)

model = create_model()
model.summary()
evaluate_model(model, 5, x_train, y_train, x_test, y_test)
models.save_model(model, "./models/digits/1/")