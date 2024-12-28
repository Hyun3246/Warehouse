## 5강-1
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

import os

if os.name == "posix":      # 맥
    sns.set("font", family = "AppleGothic")
else:
    sns.set("font", family="Malgun Gothic")

plt.rc("axes", unicode_minus =False)

df_raw = pd.read_csv("data/국가_대륙_별_상품군별_온라인쇼핑_해외직접판매액_20230216161801.csv", encoding="cp949")

df_raw["국가(대륙)별"].value_counts()
df_raw[df_raw["국가(대륙)별"] == "미국"]

# tidy data 만들기
df = df_raw.melt(id_vars=["국가(대륙)별", "상품군별", "판매유형별"], var_name="기간", value_name="백만원")

# 데이터 전처리
df["기간"].map(lambda x: int(x.split()[0]))      # 연도만 숫자로 분리
df["기간"].map(lambda x: int(x.split()[1].split("/")[0]))      # 분기만 숫자로 분리

df["백만원"] = df["백만원"].replace("-", pd.np.nan).astype(float)        # '-'를 결측치로 변경 -> 데이터 타입을 숫자로 변경할 수 있다.

df = df[(df["국가(대륙)별"] != "합계") & (df["상품군별"] != "합계")].copy()         # 불필요한 '합계' 데이터 제거

df.isnull()

# 시각화
df_total = df[df["판매유형별"] == "계"].copy()

sns.lineplot(data = df_total, x="연도", y="백만원")
sns.lineplot(data = df_total, x="연도", y="백만원", hue="상품군별")
plt.legend(bbox_to_anchor=(1.05, 1), loc=2, borderaxespad = 0.)     # 그래프 밖에 legend 추가

sns.relplot(data = df_total, x="연도", y="백만원", hue="상품군별", kind="line", col="상품군별", col_wrap=4)     # "상품군별"로 서브플롯 그리기. 화장품 값이 너무 커서 다른 값을 제대로 보기 어려움.

df_sub = df_total[df_total["상품군별"].isin(["화장품", "의류 및 패션관련 상품"])].copy()

sns.relplot(data = df_sub, x="연도", y="백만원", hue="상품군별", col="상품군별", col_wrap=4, kind="line")        # 화장품 제외하고 서브플롯 그리기
