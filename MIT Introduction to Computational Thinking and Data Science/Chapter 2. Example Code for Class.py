# Chapter 1의 코드를 이어서 활용한다.
class Food():
    '''음식을 정의하는 Food 객체'''
    def __init__(self, n, v, w):
        self.name = n
        self.value = v
        self.calories = w
        
    def getValue(self):
        return self.value
    
    def getCost(self):
        return self.calories
    
    def density(self):
        return self.getValue() / self.getCost()
    
    def __str__(self):
        return self.name + ': <' + str(self.value) + ',' + str(self.calories) + '>'


def buildMenu(names, values, calories):
    '''Food 객체를 list에 담아 menu를 생성하는 buildMenu 함수'''

    menu = []
    for i in range(len(values)):
        menu.append(Food(names[i], values[i], calories[i]))
    return menu

def greedy(items, maxCost, keyFunction):
    '''탐욕 알고리즘 정의'''
    itemsCopy = sorted(items, key = keyFunction, reverse=True)  # 우선시하는 가치인 keyFunction에 따라 정렬

    result = []

    totalValue, totalCost = 0.0, 0.0

    for i in range(len(itemsCopy)):
        if (totalCost + itemsCopy[i].getCost()) <= maxCost: # 허락된 비용보다 작은 상황이면 result에 추가
            result.append(itemsCopy[i])
            totalCost += itemsCopy[i].getCost()
            totalValue += itemsCopy[i].getValue()
    
    return (result, totalValue)

def testGreedy(items, constraint, keyFunction):
    '''탐욕 알고리즘 1회 테스트'''
    taken, val = greedy(items, constraint, keyFunction)
    print("Total value of items taken = ", val)
    
    for item in taken:
        print(' ', item)

def testGreedys(foods, maxUnits):
    '''탐욕 알고리즘 반복 테스트'''
    # value 순으로
    print("Use greedy by value to allocate", maxUnits, 'calories')
    testGreedy(foods, maxUnits, Food.getValue)
    # 비용(칼로리) 순으로
    print('\nUse greedy by cost to allocate', maxUnits, 'calories')
    testGreedy(foods, maxUnits, lambda x: 1/Food.getCost(x))    # 칼로리가 적은 순으로 정렬해야하므로 역수를 취하였음.
    # 밀도 순으로
    print("\nUse greedy by density to allocate", maxUnits, 'calories')
    testGreedy(foods, maxUnits, Food.density)

# Chapter 2 시작
def maxVal(toConsider, avail):
    '''결정 트리 구현. 
    toConsider은 아직 고려하지 않은 트리 상단 노트에 있는 물건 리스트, 
    avail은 남은 여유 공간을 의미한다'''
    if toConsider == [] or avail == 0:          # 만약 고려할 것이 없거나 여유공간이 없으면
        result =(0, ())
    elif toConsider[0].getUnits() > avail:      # 만약 고려할 것이 여유공간보다 크면
        result = maxVal(toConsider[1:], avail)
    else:                                       # 만약 고려할 것이 여유공간보다 작으면 -> 선택해야 한다
        nextItem = toConsider[0]
        withVal, withToTake = maxVal(toConsider[1:], avail - nextItem.getUnits())
        withVal += nextItem.getValue()
        withoutVal, withoutToTake = maxVal(toConsider[1:], avail)
    if withVal > withoutVal:
        result = (withVal, withToTake + (nextItem, ))
    else:
        result = (withoutVal, withoutToTake)
    
    return result

def testMaxVal(foods, maxUnits, printItems = True):
    '''MaxVal 테스트'''
    print('Use search tree to allocate', maxUnits, 'calories')
    val, taken = maxVal(foods, maxUnits)
    print('Total value of items taken =', val)
    if printItems:
        for item in taken:
            print('   ', item)

names = ['wine', 'beer', 'pizza', 'burger', 'fries', 'cola', 'apple', 'donut', 'cake']
values = [89,90,95,100,90,79,50,10]
calories = [123,154,258,354,365,150,95,195]

foods = buildMenu(names, values, calories)

testGreedys(foods, 750)
testMaxVal(foods, 750)

# 메뉴를 늘려보자
import random
def buildLargeMenu(numItems, maxVal, maxCost):
    items = []
    for i in range(numItems):
        items.append(Food(str(i), random.randint(1, maxVal), random.randint(1, maxVal)))
    return items

for numItems in range(5, 65, 5):
    items = buildLargeMenu(numItems, 90, 250)
    testMaxVal(items, 750, False)


# 피보나치 함수
def fib(n):
    if n == 0 or n == 1:
        return 1
    else:
        return fib(n- 1) + fib(n - 2)

fib(120)


# 메모를 사용해 피보나치 계산
def fastFib(n, memo = {}):
    if n == 0 or n == 1:
        return 1
    try:
        return memo[n]      # memo 딕셔너리에서 n을 찾는다
    except KeyError:        # memo 딕셔너리에 n이 없으면 이를 계산해서 딕셔너리에 저장한다.
        result = fastFib(n - 1, memo) + fastFib(n - 2, memo)
        memo[n] = result
        return result

for i in range(121):
   print('fib(' + str(i) + ') =', fastFib(i))

def fastMaxVal(toConsider, avail, memo = {}):
    """메모이제이션을 이용한 MaxVal 함수"""
    if (len(toConsider), avail) in memo:
        result = memo[(len(toConsider), avail)]
    elif toConsider == [] or avail == 0:
        result = (0, ())
    elif toConsider[0].getCost() > avail:
        result = fastMaxVal(toConsider[1:], avail, memo)
    else:
        nextItem = toConsider[0]
        withVal, withToTake = fastMaxVal(toConsider[1:], avail - nextItem.getCost(), memo)
        withVal += nextItem.getValue()
        withoutVal, withoutToTake = fastMaxVal(toConsider[1:], avail, memo)

        if withVal > withoutVal:
            result = (withVal, withToTake + (nextItem, ))
        else:
            result = (withoutVal, withoutToTake)
    memo[(len(toConsider), avail)] = result
    return result

def testMaxVal(foods, maxUnits, algorithm, printItems = True):
    print('Menu contains', len(foods), 'items')
    print('Use search tree to allocate', maxUnits,
          'calories')
    val, taken = algorithm(foods, maxUnits)
    if printItems:
        print('Total value of items taken =', val)
        for item in taken:
            print('   ', item)
          
for numItems in (5, 10, 15, 20, 25, 30, 35, 40, 45, 50):
   items = buildLargeMenu(numItems, 90, 250)
   testMaxVal(items, 750, fastMaxVal, True)
