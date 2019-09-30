import  tensorflow as tf
from tensorflow.keras import datasets, layers, Sequential, callbacks
from tensorflow.keras.preprocessing import image
from datetime import datetime

def train():
    (x, y), _ = datasets.mnist.load_data()
    x = x / 255.0

    model = Sequential([
        layers.Flatten(input_shape=(28,28), name="layer1"),
        layers.Dense(300, activation='relu', name="layer2"),
        layers.Dense(150, activation='relu', name="layer3"),
        layers.Dense(10, activation='softmax', name="output_layer")
    ])
    model.summary()

    model.compile(
        optimizer='adam',
        loss='sparse_categorical_crossentropy',
        metrics=['accuracy', 'mse', 'mae'])

    logdir='training\\logs\\' + datetime.now().strftime("%Y%m%d-%H%M%S")
    tensorboard_callback = callbacks.TensorBoard(log_dir=logdir, update_freq='batch', profile_batch = 3)

    model.fit(
        x,
        y, 
        batch_size=600,
        epochs=5, 
        callbacks=[tensorboard_callback])

    return model

def preprocess(path):
    pil = image.load_img(path, target_size=(28, 28), color_mode="grayscale")
    img = image.img_to_array(pil, data_format="channels_first") / 255.
    tensor = tf.convert_to_tensor(img)
    return img