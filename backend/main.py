import os
#ignore warning
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'

from tensorflow.keras import models
from training import create_model, evaluate_model

model = create_model()
model.summary()
evaluate_model(model, 5, 200, 55)
models.save_model(model, "./models/digits/1/")