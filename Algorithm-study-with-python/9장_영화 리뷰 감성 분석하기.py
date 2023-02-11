import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline
from sklearn.feature_extraction.text import TfidfTransformer
from sklearn.naive_bayes import MultinomialNB
from sklearn.metrics import confusion_matrix, classification_report, accuracy_score

df = pd.read_csv("moviereviews.tsv", sep='\t')
print(df.head())
print(len(df))

df.dropna(inplace=True)

blanks = []

for i, lb, rv in df.itertuples():
    if rv.isspace():
        blanks.append(i)

df.drop(blanks, inplace=True)

# 특성과 라벨 정의
X = df['review']
y = ['label']

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=42)

# 파이프라인 제작
text_clf_nb = Pipeline([('tfidf', TfidfTransformer()), ('clf', MultinomialNB())])

# 모델 훈련
text_clf_nb.fit(X_train, y_train)

predictions = text_clf_nb.predict(X_test)

print(confusion_matrix(y_test, predictions))

print(classification_report(y_test, predictions))

print(accuracy_score(y_test, predictions))