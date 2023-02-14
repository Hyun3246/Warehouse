import random
import math

# 주사위 문제 풀기
def rollDie():
    '''1~6 중에 하나 반환'''
    return random.choice([1, 2, 3, 4, 5, 6])

def testRoll(n = 10):
    '''주사위 굴리기'''
    result = ''
    for i in range(n):
        result = result + str(rollDie())
    print(result)

random.seed(0)

def runSim(goal, numTrials, txt):
    '''특정 배열이 나올 확률(수학적, 시뮬레이션 모두) 출력'''
    total = 0
    for i in range(numTrials):
        result = ''
        for j in range(len(goal)):
            result += str(rollDie())
        if result == goal:
            total += 1
    
    print("Actual probalility of {} = {}".format(txt, round(1/(6**len(goal)), 8)))
    
    estProbability = round(total/numTrials, 8)
    print("Estimated Probability of {} = {}".format(txt, round(estProbability, 8)))

runSim('11111', 1000000, '11111')


# 생일 문제 풀기
def sameDate(numPeople, numSame):
    '''생일 같은 사람 수 반환'''
    possibleDates  = range(366)
    birthdays = [0] * 366
    for p in range(numPeople):
        birthDate = random.choice(possibleDates)
        birthdays[birthDate] += 1
    
    return max(birthdays) >= numSame

def birthdayProb(numPeople, numSame, numTrials):
    '''생일이 같을 확률 반환'''
    numHits = 0
    for t in range(numTrials):
        if sameDate(numPeople, numSame):
            numHits += 1
        
    return numHits / numTrials

# 생일이 같은 사람이 2명을 확률 계산하기(여러 사람 수에 대해)
for numPeople in [10, 20, 40, 100]:
    print('For {} est.prob. of a shared birthday is {}'.format(numPeople, birthdayProb(numPeople, 2, 10000)))
    numerator = math.factorial(366)
    denom = (366*numPeople)*math.factorial(366-numPeople)
    print("Actual prob for N=100=", 1-numerator/denom)