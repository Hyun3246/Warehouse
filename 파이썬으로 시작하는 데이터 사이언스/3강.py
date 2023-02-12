import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
from IPython.display import set_matplotlib_formats

## 3강-1

# Window의 한글 폰트 설정
plt.rc('font', family='Malgun Gothic')
plt.rc('axes', unicode_minus = False)   # 마이너스 폰트 깨지는 것 대처 

# 폰트 선명하게 보이기
set_matplotlib_formats('retina')

# 데이터 로드
df = pd.read_csv("data/상가상권정보_의료기관.csv", encoding="cp949", low_memory=False)
print(df.shape)

print(df.head(3))               # head로 미리보기
print(df.tail())                # 마지막 데이터 보기
print(df.info())                # 데이터 정보 보기
print(df.columns)               # 컬럼명만 출력
print(df.isnull())              # 결측치
print(df.isnull().sum())        # 결측치가 몇 개 있는지 세어준다

null_count = df.isnull().sum()

# 결측치를 막대그래프로 변환
null_count.plot.barh(figsize = (5, 7))     # figsize를 이용해 글자가 잘 보이도록 크기 조절


# 결측치 개수로 새로운 데이터프레임 생성
df_null_count = null_count.reset_index()
df_null_count.head()
df_null_count.columns = ["컬럼명", "결측치수"]      # 컬럼명 변경
df_null_count_top = df_null_count.sort_values(by = "결측치수", ascending=False).head(10)

df["지점명"]    # 특정 컬럼만 가져오기

# 결측치가 많은 컬럼은 제거하자
drop_columns = df_null_count_top["컬럼명"].tolist()     # 결측치가 많은 컬럼 선별
df = df.drop(drop_columns, axis=1)       # axis=1로 컬럼 기준의 drop

# 기초 통계 수치
print(df["위도"].mean())   # 평균
print(df["위도"].median())  # 중앙값
print(df["위도"].max())     # 최댓값
print(df["위도"].mix())     # 최솟값
print(df["위도"].count())   # 개수
print(df["위도"].describe())    # 통계 수치 요약
print(df[["위도", "경도"]].describe())      # 두 개 컬럼 통계 수치 요약
print(df.describe(include="object"))    # 문자열 데이터 타입 요약
print(df["상권업종대분류명"].unique())      # 중복 제거한 값 보기
print(df["상권업종대분류명"].nunique())      # 중복 제거한 값 개수 세기
print(df["상권업종중분류명"].unique())      # 중복 제거한 값 보기
print(df["상권업종중분류명"].nunique())      # 중복 제거한 값 개수 세기
print(df["상권업종소분류명"].unique())      # 중복 제거한 값 보기
print(df["상권업종소분류명"].nunique())      # 중복 제거한 값 개수 세기
print(df["시도명"].value_counts(normalize=True))        # 전체에서의 비율 계산

# 시각화
city = df["시도명"].value_counts()
city_normalize = df["시도명"].value_counts(normalize=True)

city.plot.barh()
city_normalize.pie(figsize=(7, 7))