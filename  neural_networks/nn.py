import tensorflow as tf
import numpy as np

EPOCHS = 3


def generate_dataset():
    data = np.load('./mnist.npz')
    x_train = data['x_train']
    y_train = data['y_train']
    x_test = data['x_test']
    y_test = data['y_test']
    return x_train, y_train, x_test, y_test


def normalize_data(data):
    return tf.keras.utils.normalize(data)


def create_nn_model():
    model = tf.keras.models.Sequential()
    model.add(tf.keras.layers.Flatten())
    model.add(tf.keras.layers.Dense(128, activation=tf.nn.relu))
    model.add(tf.keras.layers.Dense(128, activation=tf.nn.relu))
    model.add(tf.keras.layers.Dense(10, activation=tf.nn.softmax))
    return model


x_train, y_train, x_test, y_test = generate_dataset()
x_train = normalize_data(x_train)
x_test = normalize_data(x_test)
model = create_nn_model()
model.compile(optimizer="adam", loss="sparse_categorical_crossentropy", metrics=["accuracy"])
# прогоняем на тесте
model.fit(x=x_train, y=y_train, epochs=EPOCHS)
test_loss, test_acc = model.evaluate(x=x_test, y=y_test)

# примерно 0,97
print('Результат теста = ', test_acc)