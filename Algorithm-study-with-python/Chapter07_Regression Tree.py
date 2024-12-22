import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.tree import DecisionTreeRegressor
from sklearn.metrics import mean_squared_error
from math import sqrt

dataset = pd.read_csv('auto.csv')

print(dataset.head(5))

dataset = dataset.drop(columns=['NAME'])

dataset = dataset.apply(pd.to_numeric, errors = 'coerce')
dataset.fillna(0, inplace=True)

y=dataset['MPG']
X=dataset.drop(columns=['MPG'])

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.25, random_state=0)

# 회귀 트리 알고리즘
regressor = DecisionTreeRegressor(max_depth=3)
print(regressor.fit(X_train, y_train))

y_pred = regressor.predict(X_test)
print(sqrt(mean_squared_error(y_test, y_pred)))
