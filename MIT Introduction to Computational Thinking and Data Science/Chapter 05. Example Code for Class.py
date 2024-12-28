import random, pylab
class Location(object):
    def __init__(self, x, y):
        self.x = x
        self.y = y
    
    def move(self, deltaX, deltaY):
        return Location(self.x + deltaX, self.y + deltaY)
    
    def getX(self):
        return self.x

    def getY(self):
        return self.y
    
    def disFrom(self, other):
        xDist = self.x - other.getX()
        yDist = self.y - other.getY()
        return (xDist ** 2 + yDist**2) ** 0.5
    
    def __str__(self):
        return '<' + str(self.x) + ', ' + str(self.y) + '>'
    
class Drunk(object):
    '''상속하기 위한 주정뱅이 클래스'''
    def __init__(self, name = None):
        self.name = name

    def __str__(self):
        if self != None:
            return self.name
        return 'Anonymous'
    
import random

class UsualDrunk(Drunk):
    def takeStep(self):
        stepChoices = [(0, 1), (0, -1), (1, 0), (-1, 0)]
        return random.choice(stepChoices)

class MasochistDrunk(Drunk):
    '''북쪽으로 편향된 움직임'''
    def takeStep(self):
        stepChoices = [(0.0, 1.1), (0.0, -0.9), (1.0, 0.0), (-1.0, 0.0)]
        return random.choice(stepChoices)

class Field(object):
    def __init__(self):
        self.drunks = {}
    
    def addDrunk(self, drunk, loc):
        if drunk in self.drunks:
            raise ValueError("Duplicate drunk")
        else:
            self.drunks[drunk] = loc
    
    def getLoc(self, drunk):
        if drunk not in self.drunks:
            raise ValueError('Drunk not in field')
        return self.drunks[drunk]

    def moveDrunk(self, drunk):
        if drunk not in self.drunks:
            raise ValueError("Drunk not in field")
        xDist, yDist = drunk.takeStep()
        self.drunks[drunk] = self.drunks[drunk].move(xDist, yDist)

def walk(f, d, numSteps):
    '''f는 Field, d는 Drunk'''
    start = f.getLoc(d)

    for s in range(numSteps):
        f.moveDrunk(d)

    return start.distFrom(f.getLoc(d))

def simWalks(numSteps, numTrials, dClass):
    Homer = dClass()
    origin = Location(0, 0)
    distances = []

    for t in range(numTrials):
        f = Field()
        f.addDrunk(Homer, origin)
        distances.append(round(walk(f, Homer, numTrials), 1))
    
    return distances

def drunkTest(walkLengths, numTrials, dClass):
    for numSteps in walkLengths:
        distances = simWalks(numSteps, numTrials, dClass)
        
        print(dClass.__name__, 'random walk of', numSteps, 'steps')
        print('Mean =', round(sum(distances)/len(distances), 4))
        print('Max =', max(distances), "Min =", min(distances))


## 수업에서 다루지 않은 코드들
random.seed(0)
drunkTest((10, 100, 1000, 10000), 100, UsualDrunk)
#
def simAll(drunkKinds, walkLengths, numTrials):
    for dClass in drunkKinds:
        drunkTest(walkLengths, numTrials, dClass)
        
#random.seed(0)
#simAll((UsualDrunk, MasochistDrunk),
#       (1000, 10000), 100)
#        
#xVals = [1, 2, 3, 4]
#yVals1 = [1, 2, 3, 4]
#pylab.plot(xVals, yVals1, 'b-', label = 'first')
#yVals2 = [1, 7, 3, 5]
#pylab.plot(xVals, yVals2, 'r--', label = 'second')
#pylab.legend()

class styleIterator(object):
    def __init__(self, styles):
        self.index = 0
        self.styles = styles

    def nextStyle(self):
        result = self.styles[self.index]
        if self.index == len(self.styles) - 1:
            self.index = 0
        else:
            self.index += 1
        return result
    
def simDrunk(numTrials, dClass, walkLengths):
    meanDistances = []
    for numSteps in walkLengths:
        print('Starting simulation of',
              numSteps, 'steps')
        trials = simWalks(numSteps, numTrials, dClass)
        mean = sum(trials)/len(trials)
        meanDistances.append(mean)
    return meanDistances

def simAll(drunkKinds, walkLengths, numTrials):
    styleChoice = styleIterator(('m-', 'b--', 'g-.'))
    for dClass in drunkKinds:
        curStyle = styleChoice.nextStyle()
        print('Starting simulation of', dClass.__name__)
        means = simDrunk(numTrials, dClass, walkLengths)
        pylab.plot(walkLengths, means, curStyle,
                   label = dClass.__name__)
    pylab.title('Mean Distance from Origin ('
                + str(numTrials) + ' trials)')
    pylab.xlabel('Number of Steps')
    pylab.ylabel('Distance from Origin')
    pylab.legend(loc = 'best')

#random.seed(0)
#numSteps = (10,100,1000,10000,100000)
#simAll((UsualDrunk, MasochistDrunk), numSteps, 100)
#
#pylab.plot(numSteps, pylab.array(numSteps)**0.5, 'k-.',
#           label = 'Square root of steps')
#pylab.plot(numSteps, pylab.array(numSteps)*0.05, 'g-.',
#           label = 'numSteps*0.05')
#pylab.legend(loc = 'best')

def getFinalLocs(numSteps, numTrials, dClass):
    locs = []
    d = dClass()
    for t in range(numTrials):
        f = OddField()
        f.addDrunk(d, Location(0, 0))
        for s in range(numSteps):
            f.moveDrunk(d)
        locs.append(f.getLoc(d))
    return locs

def plotLocs(drunkKinds, numSteps, numTrials):
    styleChoice = styleIterator(('k+', 'r^', 'mo'))
    for dClass in drunkKinds:
        locs = getFinalLocs(numSteps, numTrials, dClass)
        xVals, yVals = [], []
        for loc in locs:
            xVals.append(loc.getX())
            yVals.append(loc.getY())
        xVals = pylab.array(xVals)
        yVals = pylab.array(yVals)
        meanX = sum(abs(xVals))/len(xVals)
        meanY = sum(abs(yVals))/len(yVals)
        curStyle = styleChoice.nextStyle()
        pylab.plot(xVals, yVals, curStyle,
                      label = dClass.__name__ +\
                      ' mean abs dist = <'
                      + str(meanX) + ', ' + str(meanY) + '>')
    pylab.title('Location at End of Walks ('
                + str(numSteps) + ' steps)')
    pylab.ylim(-1000, 1000)
    pylab.xlim(-1000, 1000)
    pylab.xlabel('Steps East/West of Origin')
    pylab.ylabel('Steps North/South of Origin')
    pylab.legend(loc = 'lower center')

#random.seed(0)
#plotLocs((UsualDrunk, MasochistDrunk), 10000, 1000)

class OddField(Field):
    def __init__(self, numHoles = 1000,
                 xRange = 100, yRange = 100):
        Field.__init__(self)
        self.wormholes = {}
        for w in range(numHoles):
            x = random.randint(-xRange, xRange)
            y = random.randint(-yRange, yRange)
            newX = random.randint(-xRange, xRange)
            newY = random.randint(-yRange, yRange)
            newLoc = Location(newX, newY)
            self.wormholes[(x, y)] = newLoc

    def moveDrunk(self, drunk):
        Field.moveDrunk(self, drunk)
        x = self.drunks[drunk].getX()
        y = self.drunks[drunk].getY()
        if (x, y) in self.wormholes:
            self.drunks[drunk] = self.wormholes[(x, y)]
            
#TraceWalk using oddField          
def traceWalk(fieldKinds, numSteps):
    styleChoice = styleIterator(('b+', 'r^', 'ko'))
    for fClass in fieldKinds:
        d = UsualDrunk()
        f = fClass()
        f.addDrunk(d, Location(0, 0))
        locs = []
        for s in range(numSteps):
            f.moveDrunk(d)
            locs.append(f.getLoc(d))
        xVals, yVals = [], []
        for loc in locs:
            xVals.append(loc.getX())
            yVals.append(loc.getY())
        curStyle = styleChoice.nextStyle()
        pylab.plot(xVals, yVals, curStyle,
                   label = fClass.__name__)
    pylab.title('Spots Visited on Walk ('
                + str(numSteps) + ' steps)')
    pylab.xlabel('Steps East/West of Origin')
    pylab.ylabel('Steps North/South of Origin')
    pylab.legend(loc = 'best')

#random.seed(0)
#traceWalk((Field, OddField), 500)


