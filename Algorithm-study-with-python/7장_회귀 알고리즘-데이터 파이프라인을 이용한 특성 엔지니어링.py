import pandas as pd
from sklearn.model_selection import train_test_split

dataset = pd.read_csv('auto.csv')

print(dataset.head(5))

dataset = dataset.drop(columns=['NAME'])

dataset = dataset.apply(pd.to_numeric, errors = 'coerce')
dataset.fillna(0, inplace=True)

y=dataset['MPG']
X=dataset.drop(columns=['MPG'])

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.25, random_state=0)