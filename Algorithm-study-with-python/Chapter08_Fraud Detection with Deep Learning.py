import random
import numpy as np
import tensorflow as tf

# 뉴럴 네트워크 정의
def createTemplate():
    return tf.keras.models.Sequential([tf.keras.layers.Flatten(),
    tf.keras.layers.Dense(128, activation='relu'),
    tf.keras.layers.Dropout(0.15),
    tf.keras.layers.Dense(128, activation='relu'),
    tf.keras.layers.Dropout(0.15),
    tf.keras.layers.Dense(64, activation='relu')])

# 데이터 준비
def prepareData(inputs: np.ndarray, labels: np.ndarray):
    classNumbers = 10
    digitalIdx = [np.where(labels == i)[0] for i in range(classNumbers)]
    pairs = list()
    labels = list()
    n = min([len(digitalIdx[d]) for d in range(classNumbers)]) - 1
    for d in range(classNumbers):
        for i in range(n):
            z1, z2 = digitalIdx[d][i], digitalIdx[d][i + 1]
            pairs += [[inputs[z1], inputs[z2]]]
            inc = random.randrange(1, classNumbers)
            dn = (d + inc) % classNumbers
            z1, z2 = digitalIdx[d][i], digitalIdx[dn][i]
            pairs += [[inputs[z1], inputs[z2]]]
            labels += [1, 0]
    return np.array(pairs), np.array(labels, dtype=np.float32)

# 데이터셋 준비
(x_train, y_train), (x_test, y_test) = tf.keras.datasets.mnist.load_data()
x_train = x_train.astype(np.float32)
x_test = x_test.astype(np.float32)
x_train /= 255
x_test /= 255
input_shape = x_train.shape[1:]
train_pairs, tr_labels = prepareData(x_train, y_train)
test_pairs, test_labels = prepareData(x_test, y_test)

# 샴 뉴럴 네트워크 시스템 구성 브랜치 제작
base_network = createTemplate()
input_a = tf.keras.layers.Input(shape=input_shape)
encoder1 = base_network(input_a)
input_b = tf.keras.layers.Input(shape=input_shape)
encoder2 = base_network(input_b)

# 두 문서 간 유사도 구현
distance = tf.keras.layers.Lambda(lambda embeddings: tf.keras.backend.abs(embeddings[0] - embeddings[1]))([encoder1, encoder2])
measure0fSimilarity = tf.keras.layers.Dense(1, activation='sigmoid')(distance)

# 모델 훈련
model = tf.keras.models.Model([input_a, input_b], measure0fSimilarity)
model.compile(loss='binary_crossentropy', optimizer=tf.keras.optimizers.Adam(), metrics=['accuracy'])

model.fit([train_pairs[:, 0], train_pairs[:, 1]], tr_labels, batch_size=128, epochs=10, validation_data=([test_pairs[:, 0], test_pairs[:, 1]], test_labels))
