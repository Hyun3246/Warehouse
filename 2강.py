import pandas as pd
# glob는 유닉스 기반의 경로명 확장
from glob import glob

# 하나의 파일 가져오기
file_name = glob("data/*.csv")
print(file_name[0])
print(pd.read_csv(file_name[0], encoding="cp949"))

# 여러 파일 한 번에 로드하기
file_csv = glob("data/store/*_*_*.csv")    # 파일명의 규칙에 따라서 가져올 수 있다.

file_list = []
for file_csv_name in file_csv:
    print(file_csv_name)
    temp = pd.read_csv(file_csv_name, low_memory=False)
    file_list.append(temp)

# 하나의 데이터 프레임으로 합치기
df = pd.concat(file_list)

# 데이터셋 모양 확인
print(df.shape)