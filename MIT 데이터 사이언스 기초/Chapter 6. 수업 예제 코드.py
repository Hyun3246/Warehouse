import random

class FairRoulette():
    '''공정한 룰렛'''
    def __init__(self):
        self.pockets = []
        for i in range(37):
            self.pockets.append(i)
        self.ball = None
        self.pocketsOdds = len(self.pockets) - 1

    def spin(self):
        self.ball = random.choice(self.pockets)
    
    def betPocket(self, pocket, amt):
        if str(pocket) == str(self.ball):
            return amt * self.pocketsOdds
        else:
            return -amt
    
    def __str__(self):
        return "Fair Roulette"

def playRoulette(game, numSpins, pocket, bet, toPrint):
    totPocket = 0
    for i in range(numSpins):
        game.spin()
        totPocket += game.betPocket(pocket, bet)

    if toPrint:
        print(numSpins, "spins of", game)
        print("Expected return betting", pocket, '=', str(100*totPocket/numSpins) + "%\n")
    
    return (totPocket / numSpins)

random.seed(0)

game = FairRoulette()

for numSpins in (100, 1000000):
    for i in range(3):
        playRoulette(game, numSpins, 2, 1, True)

class EuRoulette(FairRoulette):
    '''유럽식 룰렛. 0이 하나다.'''
    def __init__(self):
        FairRoulette.__init__(self)
        self.pockets.append('0')
    
    def __str__(self):
        return "European Roulette"

class AmRoulette(EuRoulette):
    '''미국식 룰렛. 00도 있다'''
    def __init__(self):
        EuRoulette.__init__(self)
        self.pockets.append('00')
    
    def __str__(self):
        return 'American Roulette'

def findPocketReturn(game, numTrials, trialSize, toPrint):
    pocketReturns = []
    for t in range(numTrials):
        trialVals = playRoulette(game, trialSize, 2, 1, toPrint)
        pocketReturns.append(trialVals)
    return pocketReturns

# 경험적인 규칙 적용    
random.seed(0)
numTrials = 20
resultDict = {}
games = (FairRoulette, EuRoulette, AmRoulette)

for G in games:
    resultDict[G().__str__()] = []

for numSpins in (100, 1000, 10000):
    print("\nSimulate betting a pocket for {} trials of {} spins each".format(numTrials, numSpins))
    
    for G in games:
        pocketReturns = findPocketReturn(G(), 20, numTrials, False)

        expReturn = 100*sum(pocketReturns)/len(pocketReturns)
        print('Exp. return for', G(), '=', str(round(expReturn, 4)) + '%')
             

def getMeanAndStd(X):
    mean = sum(X)/float(len(X))
    tot = 0.0
    for x in X:
        tot += (x - mean)**2
    std = (tot/len(X))**0.5
    return mean, std
