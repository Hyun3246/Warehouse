import sklearn
import numpy as np
from lime.lime_tabular import LimeTabularExplainer as ex
import pickle
from sklearn.ensemble import RandomForestRegressor
from matplotlib import pyplot as plt

# 주택 가격 예측 모델
pkl_file = open("housing.pkl", "rb")
housing = pickle.load(pkl_file)
pkl_file.close()
housing['feature_names']

# 모델 훈련
X_train, X_test, y_train, y_test = sklearn.model_selection.train_test_split(housing.data, housing.target)

regressor = RandomForestRegressor()
regressor.fit(X_train, y_train)

cat_col = [i for i, col in enumerate(housing.data.T) if np.unique(col).size < 10]

# LIME 해석 모델 생성
myexplainer = ex(X_train, feature_names=housing.feature_names, class_names = ['price'], categorical_features=cat_col, mode='regression')

plt.tight_layout()

# 테스트 케이스 선정
for i in [1, 35]:
    exp = myexplainer.explain_instance(X_test[i], regressor.predict, num_features=10)
    exp.as_pyplot_figure()
    plt.tight_layout()

plt.show()