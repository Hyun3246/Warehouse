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


## 3강-2
a = sns.countplot(data=df, y = "시도명")        # seaborn으로 그려보기. value count를 비롯한 통계 처리를 그래프 생성 시에 알아서 진행한다. 변수에 넣으면 그래프만 깔끔하게 도출


c = df["상권업종대분류명"].value_counts()
n = df["상권업종중분류명"].value_counts(normalize=True)

c.plot.bar(rot = 0)     # rot로 글자를 돌려준다

n.plot.pie()        # 판다스로 그려보기

d = df["상권업종소분류명"].value_counts()
d.plot.barh(figsize=(7, 8))    # 판다스로 그려보기


# 데이터 색인하기
df_medical = df[df["상권업종중분류명"] == "약국/한약방"].copy()      # 특정 데이터만 추출해서 새로운 데이터프레임. copy를 사용해서 df의 변화를 막는다.
m = df["상권업종대분류명"] == "의료"        # boolen indexing
df.loc[m, "상권업종중분류명"]            # 행, 열 골라서 가져오기
df.loc[df["상권업종대분류명"] == "의료", "상권업종중분류명"].value_counts()

df_medi = df[df["상권업종중분류명"] == "유사의료업"]      # 유사의료업만 모으기

df["상호명"].value_counts().head()      # 가장 많은 상호명이 무엇일까

df_medi["상호명"].value_counts().head(10)

df_seoul_drug = df[(df["상권업종소분류명"] == "약국") & (df["시도명"] == "서울특별시")]     # 조건 2개

e = df_seoul_drug["시군구명"].value_counts()
n = df_seoul_drug["시군구명"].value_counts(normalize=True)

e.plot.bar()

df_seoul_hospital = df[(df["상권업종소분류명"] == "종합병원") & (df["시도명"] == "서울특별시")].copy()     # 서울특별시의 종합병원만 보기

df_seoul_hospital["시군구명"].value_counts()
df_seoul_hospital[df_seoul_hospital["상호명"].str.contains('종합병원')]    # 종합병원이 들어간 텍스트만 가져오기
df_seoul_hospital[~df_seoul_hospital["상호명"].str.contains('종합병원')]    # 종합병원이 안 들어간 텍스트만 가져오기

df_seoul_hospital[df_seoul_hospital["상호명"].str.contains("꽃배달")]       # 상호명에 꽃배달이 들어간 데이터
df_seoul_hospital[df_seoul_hospital["상호명"].str.contains("의료기")]       # 상호명에 의료기가 들어간 데이터
drop_row = df_seoul_hospital[df_seoul_hospital["상호명"].str.contains("꽃배달|의료기|장례식장|상담소|어린이집")].index     # 여러 개 텍스트 조건
drop_row = drop_row.tolist()
drop_row2 = df_seoul_hospital[df_seoul_hospital["상호명"].str.endswith("의원")].index   # 의원으로 끝나는 상호명
drop_row2 = drop_row2.tolist()
drop_row = drop_row + drop_row2

df_seoul_hospital.drop(drop_row)        # 종합병원으로 보기 어려운 데이터 삭제

df_seoul_hospital["시군구명"].value_counts()    # 진짜 종합병원 시군구별 개수
plt.figure(figsize=(15, 4))
sns.countplot(data=df_seoul_hospital, x = "시군구명", order=df_seoul_hospital["시군구명"].value_counts().index)

df_seoul = df[df["시도명"] == "서울특별시"].copy()
df_seoul["시군구명"].value_counts().plot.bar(figsize=(10, 4))
plt.figure(figsize=(15, 4))
sns.countplot(data=df_seoul, x="시군구명")

df_seoul[["경도", "위도", "시군구명"]].plot.scatter(x="경도", y="위도", figsize = (8, 7), grid=True)     # 서울시 시도처럼 그려진다

sns.scatterplot(data=df_seoul, x='경도', y="위도", hue="시군구명")      # hue 값에 따라서 색상 달라짐
sns.scatterplot(data=df, x='경도', y="위도", hue="시도명")      # 전국 지도처럼 그려진다


# 실제 지도에 나타내기
import folium

folium.Map()        # 세계지도



map = folium.Map(location = [df_seoul_hospital["위도"].mean(), df_seoul_hospital["경도"].mean()], zoom_start = 12)     # 데이터의 위도, 경도 평균치로 서울 지도 나타내기, zoom_start로 zoom 정도 설정

# 지도에 마커 추가
for n in df_seoul_hospital.index:
    name = df_seoul_hospital.loc[n, "상호명"]
    address = df_seoul_hospital.loc[n, "도로명주소"]
    popup = f"{name} - {address}"
    location = [df_seoul_hospital.loc[n, "위도"], df_seoul_hospital.loc[n, "경도"]]
    folium.Marker(location=location, popup=popup).add_to(map)

map
