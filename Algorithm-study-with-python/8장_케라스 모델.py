import tensorflow as tf
from keras.models import Sequential
from keras import Input
from keras.layers import Flatten, Dense, Activation, Dropout
from keras.datasets import mnist

(x_train, y_train), (x_test, y_test) = mnist.load_data()

# 함수형 API
model = Sequential([
    Flatten(input_shape = (128, 128)),
    Dense(128, activation='relu'),
    Dropout(0.2),
    Dense(10)
])

# 순차형 API
inputs = Input(shape=(128, 128))
x = Flatten()(inputs)
x = Dense(128, activation='relu')(x)
x = Dropout(0.2)(x)
x = Dense(10)(x)
model = tf.keras.Model(inputs = inputs, outputs = x)


# 학습 프로세스 정의
optimizer = tf.keras.optimizer.Adam(0.001)
loss = tf.keras.losses.SparseCategoricalCrossentropy(from_logits = True)

model.compile(optimizer=optimizer, loss=loss, metrics=['accuracy'])

# 훈련
model.fit(x_train, y_train, batch_size = 128, epochs=10)

# 모델 정확도 측정
model.evaluate(x_test, y_test, batch_size=128)