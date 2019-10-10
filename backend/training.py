import  tensorflow as tf
from tensorflow.keras import datasets, layers, Sequential, callbacks, models
from tensorflow.keras.preprocessing import image
from tensorflow.keras.preprocessing.image import ImageDataGenerator
from tensorflow.keras.utils import to_categorical
from datetime import datetime
from matplotlib import pyplot
from sklearn.model_selection import StratifiedKFold
from numpy import mean, std, expand_dims


def load_data():
    (x_train, y_train), (x_test, y_test) = datasets.mnist.load_data()
    return x_train, y_train, x_test, y_test

def display_images(x, y, rows=1, cols=1):
    for i in range(rows*cols):
        pyplot.subplot(rows, cols, i+1)
        pyplot.title(str(y[i]))
        pyplot.imshow(x[i], cmap=pyplot.get_cmap('gray'))
    pyplot.show()

def normalize_data(x):
    expanded = expand_dims(x, 4)
    return expanded / 255

def create_model():
    model = Sequential([
        # layers.Conv2D(32, kernel_size=(3,3), activation='relu', input_shape=(28,28,1)),
        # layers.Conv2D(64, kernel_size=(3,3), activation='relu'),
        # layers.MaxPooling2D(pool_size=(2,2)),
        # layers.Dropout(0.25),
        layers.Flatten(input_shape=(28,28,1)),
        layers.Dense(128, activation='relu'),
        layers.Dense(64, activation='relu'),
        layers.Dense(32, activation='relu'),
        layers.Dense(10, activation='softmax')
    ])

    model.compile(
        optimizer='adam',
        loss='sparse_categorical_crossentropy',
        metrics=['accuracy'])

    return model

def evaluate_model(model, epochs, x_train, y_train, x_test, y_test):
    logdir='logs\\' + datetime.now().strftime("%Y%m%d-%H%M%S")
    tensorboard_callback = callbacks.TensorBoard(log_dir=logdir, update_freq='batch', profile_batch = 3)

    generator = ImageDataGenerator(
        zoom_range=0.5,
        rotation_range=30,
        width_shift_range=4,
        height_shift_range=4)

    model.fit_generator(generator.flow(x=x_train, y=y_train, batch_size=60),
        steps_per_epoch=1000,
        epochs=epochs,
        callbacks=[tensorboard_callback],
        validation_data=(x_test, y_test),
        validation_freq=1)
    # model.fit(
    #     x=x_train,
    #     y=y_train, 
    #     batch_size=600,
    #     epochs=epochs,
    #     callbacks=[tensorboard_callback],
    #     validation_data=(x_test, y_test),
    #     validation_freq=1)

def preprocess(path):
    pil = image.load_img(path, color_mode="grayscale")
    array = image.img_to_array(pil, data_format="channels_last") 
    reshaped = array.reshape(1, pil.width, pil.height, 1)
    resized = tf.image.resize(reshaped, size=[28,28], method='gaussian')
    return resized/255
    


# def evaluate_model(x_train, y_train, n_folds=5):
#     # logdir='training\\logs\\' + datetime.now().strftime("%Y%m%d-%H%M%S")
#     # tensorboard_callback = callbacks.TensorBoard(log_dir=logdir, update_freq='batch', profile_batch = 3)
#     accuracies = list()
#     kfold = StratifiedKFold(n_folds, shuffle=True, random_state=1)
#     for i_train, i_test in kfold.split(x_train, y_train):
#         x_train_fold = x_train[i_train]
#         y_train_fold = y_train[i_train]
#         x_test_fold = x_train[i_test] 
#         y_test_fold = y_train[i_test]

#         model = create_model()
        
#         history = model.fit(
#             x=x_train_fold,
#             y=y_train_fold, 
#             batch_size=600,
#             epochs=5,
#             #callbacks=[tensorboard_callback],
#             validation_data=(x_test_fold, y_test_fold))
#         accuracies.append({"train": history.history['accuracy'], "test": history.history['val_accuracy']})

#     return accuracies


# def display_results(accuracies):
#     n_folds = len(accuracies)
#     test_accuracies = list()
#     for i_fold in range(n_folds):
#         pyplot.subplot(n_folds, 1, i_fold+1)
#         pyplot.title(str(i_fold+1))
#         pyplot.xlabel("epochs")
#         pyplot.ylabel("accuracy")
#         pyplot.plot(accuracies[i_fold]["train"], color='green', label='train')
#         pyplot.plot(accuracies[i_fold]["test"], color='red', label='test')
#         test_accuracies.append(accuracies[i_fold]["test"][-1])
#     pyplot.show()
#     print('test accuracy [%d folds] = %.3f +/- %.3f' % (n_folds, mean(test_accuracies)*100, std(test_accuracies)*100))
#     # pyplot.boxplot(test_accuracies)
#     # pyplot.show()


# casted = tf.dtypes.cast(resized[0,:,:,:].numpy().reshape(280, 280, 1), dtype=tf.uint8)
    # encoded = tf.io.encode_jpeg(casted)
    # tf.io.write_file("C:\\Users\\sdf\\Desktop\\ML\\code\\tensorflow\\resized.jpeg", encoded)