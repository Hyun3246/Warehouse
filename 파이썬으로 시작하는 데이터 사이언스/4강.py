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


df_sample = df.sample(1000, random_state=1)     # seaborn은 시간이 오래 걸림. Sample을 만들자.(random_state를 지정해서 항상 같은 데이터 추출)

sns.countplot(x = "음주여부", data = df)
sns.countplot(data = df, x = "음주여부", hue = "성별코드")
sns.countplot(data = df, x = "연령대코드 (5세단위)", hue = "음주여부")
sns.countplot(data = df, x = "신장 (5Cm단위)")

sns.barplot(data=df, x="연령대코드 (5세 단위)", y="총콜레스테롤", hue = "음주여부")       # barplot으로 그리기, 평균 값들을 표시
plt.figure(figsize=(15, 4))
sns.barplot(data=df, x="연령대코드 (5세 단위)", y="총콜레스테롤", hue = "흡연상태")       # barplot으로 그리기, 평균 값들을 표시

sns.barplot(data=df_sample, x="연령대코드 (5세 단위)", y = "트리글리세라이드", hue="음주여부", ci = "sd")       # ci로 신뢰구간 조절, sd는 표준편차

sns.barplot(data=df_sample, x="연령대코드 (5세 단위)", y = "체중 (5Kg 단위)", hue="음주여부", ci = None)

## 4강 - 2
plt.figure(figsize=(15, 4))
sns.lineplot(data=df_sample, x="연령대코드 (5세 단위)", y = "체중 (5Kg 단위)", hue="음주여부", ci = 'sd')       # 그림자로 신뢰구간 표시
sns.lineplot(data=df_sample, x="연령대코드 (5세 단위)", y = "신장(5Cm단위)", hue="음주여부", ci = 'sd')
sns.pointplot(data=df_sample, x="연령대코드 (5세 단위)", y = "신장(5Cm단위)", hue="음주여부", ci = 'sd')
sns.lineplot(data=df, x="연령대코드 (5세 단위)", y = "신장(5Cm단위)", hue="음주여부", ci = None)

sns.boxplot(data=df, x="신장(5Cm단위)", y="체중(5Kg 단위)", hue='음주여부')         # boxplot 그리기
sns.violinplot(data = df, x="신장(5Cm단위)", y="체중(5Kg 단위)", hue="음주여부")
sns.violinplot(data = df, x="신장(5Cm단위)", y="체중(5Kg 단위)", hue="음주여부", split =True)       # split으로 하나의 plot을 두 개로 쪼개기
sns.swarmplot(data=df_sample, x = "신장(5Cm단위)", y = "체중(5Kg 단위)", hue='음주여부')       # 산점도로 나타내기

sns.lmplot(data = df_sample, x="연령대코드 (5세 단위)", y='혈색소', hue = "음주여부", col="성별코드")       # 회귀선 그리기, col로 여러 개의 컬럼 나누어서 그리기

sns.scatterplot(data=df_sample, x="(혈청지오치)AST", y="(혈청지오티)ALT", hue="음주여부")       

sns.lmplot(data=df_sample, x="신장 (5Cm단위)", y="체중(5Kg 단위)", hue = "성별코드", col="음주여부")        # 하나의 그래프에 모아서 시각화하기(신장과 체중에 따른 상관관계 그래프를 그리며, 음주 여부에 따라 그래프를 나누어 나타냄. 성별에 따라 그래프의 색이 달라짐)

sns.lmplot(data=df_sample, x="수축기혈압", y="이완기혈압", hue = "음주여부")

sns.lmplot(data=df_sample, x="(혈청지오티)AST", y="(혈청지오티)ALT", hue = "음주여부", robust = True)       # robust로 이상치 제거

# 이상치 제거하기
df_ASLT = df_sample[(df_sample["(혈청지오티)AST"] < 400) & (df_sample["(혈청지오티)ALT"] < 400)]        # 이상치 제거
sns.lmplot(data = df_ASLT, x = "(혈청지오티)AST", y = "(혈청지오티)ALT", hue = "음주여부", ci = None)

df_ASLT_high = df[(df["(혈청지오티)AST"] >= 400) | (df_sample["(혈청지오티)ALT"] >= 400)]        # 이상치 보기

# distplot
df_chol = df[df["총콜레스테롤"].notnull(), "총콜레스테롤"]
sns.distplot(df_chol, bins=100)        # 히스토그램과 곡선
plt.axvline(df_sample["총콜레스테롤"].mean(), linestyle = ":")        # 그래프에 '콜레스테롤' 평균 선 나타내기
sns.distplot(df.loc[df["총콜레스테롤"].notnull() & (df["음주여부"] == 1)])          # distplot에는 시리즈형태가 들어가야 함.
sns.kdeplot(df.loc[df["총콜레스테롤"].notnull() & (df["음주여부"] == 1)])          # 히스토그램 제외하고 곡선만 그리기


# 상관 관계 파악
columns = ["연령대코드 (5세 단위)", "체중(5Kg 단위)", "신장(5Cm단위)", "허리둘레",
            "시력(좌)", "시력(우)", "청력(좌)", "청력(우)", "수축기혈압",
            "이완기혈압", "식전혈당(공복혈당)", "총콜레스테롤", "트리글리세리드",
            "HDL콜레스테롤", "LDL콜레스테롤", "혈색소", "요단백", "혈청크레아티닌",
            "(혈청지오티)AST", "(혈청지오티)ALT", "감마지피티", "흡연상태", "음주여부"]

df_small = df_sample[columns]
df_corr = df.small.corr()             # pearson 상관 계수 테이블 구하기

df_corr["신장(5Cm단위)"].sort_values()

df_corr.loc[df_corr["신장(5Cm단위)"] > 0.3, "신장(5Cm단위)"]        # 상관 계수가 특정 이상인 데이터만 추출

# heatmap
sns.heatmap(df_corr)
sns.heatmap(df_corr, annot = True, fmt = ".2f", cmap = "Blues")     # annot으로 숫자 표시, fmt로 소수점 조절, cmap으로 색상 설정

