import  tensorflow as tf
from tensorflow.keras import datasets, layers, Sequential, callbacks, models
from tensorflow.keras.preprocessing import image
from tensorflow.keras.preprocessing.image import ImageDataGenerator
from tensorflow.keras.utils import to_categorical
from datetime import datetime
from matplotlib import pyplot
from numpy import mean, std, expand_dims


def create_model():
    model = Sequential([
        layers.Flatten(input_shape=(28,28,1)),
        layers.Dense(128, activation='relu'),
        layers.Dense(32, activation='relu'),
        layers.Dense(10, activation='softmax')
    ])

    model.compile(
        optimizer='adam',
        loss='sparse_categorical_crossentropy',
        metrics=['accuracy'])

    return model

def evaluate_model(model, epochs, steps_per_epoch, batch_size):
    logdir='logs\\' + datetime.now().strftime("%Y%m%d-%H%M%S")
    tensorboard_callback = callbacks.TensorBoard(log_dir=logdir, update_freq='batch', profile_batch = 3)

    gen = ImageDataGenerator(
        rescale=1./255,
        data_format="channels_last",
        zoom_range=0.4,
        rotation_range=45)

    training_it = gen.flow_from_directory(
        "./images/training",
        target_size=(28, 28),
        color_mode='grayscale',
        class_mode='binary',
        batch_size=batch_size,
        # save_to_dir="./images/training_augmented",
        # save_format='png',
        interpolation='nearest')

    validation_it = gen.flow_from_directory(
        "./images/training",
        target_size=(28, 28),
        color_mode='grayscale',
        class_mode='binary',
        batch_size=batch_size,
        interpolation='nearest')

    model.fit_generator(training_it,
        steps_per_epoch=steps_per_epoch,
        epochs=epochs,
        callbacks=[tensorboard_callback],
        validation_data=validation_it,
        validation_freq=1)

def preprocess(path):
    pil = image.load_img(path, color_mode="grayscale")
    array = image.img_to_array(pil, data_format="channels_last") 
    reshaped = array.reshape(1, pil.width, pil.height, 1)
    resized = tf.image.resize(reshaped, size=[28,28], method='gaussian')
    return resized/255