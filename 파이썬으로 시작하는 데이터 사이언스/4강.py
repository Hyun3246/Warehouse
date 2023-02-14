## 4강 - 1
import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt

# 폰트 설정
import os


if os.name == "posix":      # 맥
    plt.rc("font", family = "AppleGothic")
else:
    plt.rc("font", family="Malgun Gothic")

plt.rc("axes", unicode_minus =False)

df = pd.read_csv("data/NHIS_OPEN_GJ_2017_v1.1.csv", encoding="cp949")

df.shape

df.head()

df.info()       # 메모리 사용을 확인하자

df.dtypes     # 데이터 타입만 출력

df.isnull().sum()       # 결측치 개수 세기
df.isna().sum()         # isnull()과 동일

df.isnull().sum().plot.barh(figsize = (10, 9))

df[["(혈청지오치)ALT", "(혈청지오치)AST"]].head()
df[["(혈청지오치)ALT", "(혈청지오치)AST"]].info()
df[["(혈청지오치)ALT", "(혈청지오치)AST"]].describe()

df["성별코드"].value_counts()
df["흡연상태"].value_counts()


# 그룹화하기, 피벗테이블
df.groupby(["성별코드"])["가입자일련번호"].count()
df.groupby(["성별코드", "음주여부"])["가입자일련번호"].count()      # 여러 컬럼으로 그룹화, 시리즈로 반환

df.groupby(["성별코드", "음주여부"])["감마지티피"].mean()
df.groupby(["성별코드", "음주여부"])["감마지티피"].describe()

df.groupby(["성별코드", "음주여부"])["감마지티피"].agg(["count", "mean", "median"])


df.pivot_table(index="음주여부", values="가입자일련번호", aggfunc="count")        # 연산을 동반하는 테이블 형태 변경, 데이터프레임으로 반환, 직관적인 사용법

pd.pivot_table(df, index="음주여부", values="감마지티피", aggfunc=["mean", "median"])   # aggfunc에 여러 개의 통계치 사용
pd.pivot_table(df, index="성별코드", values="감마지티피", aggfunc=["mean", "median"])   # aggfunc에 여러 개의 통계치 사용


# 시각화
h = df.hist(figsize=(12, 12))       # 전체 데이터에 대한 히스토그램
h = df.iloc[:, 12:24].hist(figsize=(12, 12), bins=100)        # loc로 행과 열을 슬라이싱, iloc는 숫자로 슬라이싱 가능, bin으로 막대 개수 조절 가능
h = df.iloc[:, :24].hist(figsize=(12, 12), bins=100)        # loc로 행과 열을 슬라이싱, iloc는 숫자로 슬라이싱 가능


df.sample(1000, random_state=1)     # seaborn은 시간이 오래 걸림. Sample을 만들자.(random_state를 지정해서 항상 같은 데이터 추출)

sns.countplot(x = "음주여부", data = df)
sns.countplot(data = df, x = "음주여부", hue = "성별코드")
sns.countplot(data = df, x = "연령대코드 (5세단위)", hue = "음주여부")
sns.countplot(data = df, x = "신장 (5Cm단위)")

sns.barplot(data=df, x="연령대코드 (5세 단위)", y="총콜레스테롤", hue = "음주여부")       # barplot으로 그리기, 평균 값들을 표시
plt.figure(figsize=(15, 4))
sns.barplot(data=df, x="연령대코드 (5세 단위)", y="총콜레스테롤", hue = "흡연상태")       # barplot으로 그리기, 평균 값들을 표시

sns.barplot(data=df.sample, x="연령대코드 (5세 단위)", y = "트리글리세라이드", hue="음주여부", ci = "sd")       # ci로 신뢰구간 조절, sd는 표준편차

sns.barplot(data=df.sample, x="연령대코드 (5세 단위)", y = "체중 (5Kg 단위)", hue="음주여부", ci = None)