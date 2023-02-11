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

names = ['wine', 'beer', 'pizza', 'burger', 'fries', 'cola', 'apple', 'donut', 'cake']
values = [89,90,95,100,90,79,50,10]
calories = [123,154,258,354,365,150,95,195]

foods = buildMenu(names, values, calories)

testGreedys(foods, 750)