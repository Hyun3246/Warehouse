import random

# 암 환자 지역 검증 코드
numCasesPerYear = 36000
numYears = 3
stateSize = 10000
communitySize = 10
numCommunities = stateSize // communitySize

numTrials = 100
numGreater = 0

# 111번 지역에서 3년간 143명 이상의 환자가 나올 확률 계산
for t in range(numTrials):
    locs = [0] * numCommunities
    for i in range(numYears * numCasesPerYear):
        locs[random.choice(range(numCommunities))] += 1
    if locs[111] >= 143:
        numGreater += 1

prob = round(numGreater / numTrials , 4)
print("Est. probability of region 111 having at least 143 cases =", prob)

# 어느 한 지역에서 3년간 143명 이상의 환자가 나올 확률 계산
anyRegion = 0
for trial in range(numTrials):
    locs = [0] * numCommunities
    for i in range(numYears * numCasesPerYear):
        locs[random.choice(range(numCommunities))] += 1
    if max(locs) >= 143:
        anyRegion += 1
print(anyRegion)
aProb = round(anyRegion/numTrials, 4)
print("Est. probability of some region having at least 143 cases =", aProb)