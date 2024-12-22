import numpy as np
import pandas as pd
from sklearn.preprocessing import LabelEncoder
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score
from sklearn.linear_model import LogisticRegression


df = pd.read_csv('weather.csv')



le = LabelEncoder()
df = df.dropna()
df.shape
df.WindGustDir = le.fit_transform(df.WindGustDir)
df.WindDir3pm = le.fit_transform(df.WindDir3pm)
df.WindDir9am = le.fit_transform(df.WindDir9am)

print(df.columns)
print(df.iloc[:, 0:12].head())

x = df.drop(['Date', 'RainTomorrow'], axis=1)
y = df['RainTomorrow']

train_x, train_y, test_x, test_y = train_test_split(x, y, test_size=0.2, random_state=2)

print(train_x.shape)
print(train_y.shape)

model = LogisticRegression()

print(model.fit(train_x, test_x))

predict = model.predict(train_y)

print(accuracy_score(predict, test_y))
