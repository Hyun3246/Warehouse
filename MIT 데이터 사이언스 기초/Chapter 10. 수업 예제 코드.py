import random, pylab, numpy

# 지난 강의 코드 ##############################################
def getData(fileName):
    dataFile = open(fileName, 'r')
    distances = []
    masses = []
    dataFile.readline() #discard header
    for line in dataFile:
        d, m = line.split()
        distances.append(float(d))
        masses.append(float(m))
    dataFile.close()
    return (masses, distances)
    
def labelPlot():
    pylab.title('Measured Displacement of Spring')
    pylab.xlabel('|Force| (Newtons)')
    pylab.ylabel('Distance (meters)')

def plotData(fileName):
    xVals, yVals = getData(fileName)
    xVals = pylab.array(xVals)
    yVals = pylab.array(yVals)
    xVals = xVals*9.81  #acc. due to gravity
    pylab.plot(xVals, yVals, 'bo',
               label = 'Measured displacements')
    labelPlot()
    
def fitData(fileName):
    xVals, yVals = getData(fileName)
    xVals = pylab.array(xVals)
    yVals = pylab.array(yVals)
    xVals = xVals*9.81 #get force
    pylab.plot(xVals, yVals, 'bo',
               label = 'Measured points')
    labelPlot()                 
    a,b = pylab.polyfit(xVals, yVals, 1)
    estYVals = a*pylab.array(xVals) + b
    print('a =', a, 'b =', b)
    pylab.plot(xVals, estYVals, 'r',
               label = 'Linear fit, k = '
               + str(round(1/a, 5)))
    pylab.legend(loc = 'best')
    
#fitData('springData.txt')

   
def fitData1(fileName):
    xVals, yVals = getData(fileName)
    xVals = pylab.array(xVals)
    yVals = pylab.array(yVals)
    xVals = xVals*9.81 #get force
    pylab.plot(xVals, yVals, 'bo',
               label = 'Measured points')
    labelPlot()                 
    model = pylab.polyfit(xVals, yVals, 1)
    estYVals = pylab.polyval(model, xVals)
    pylab.plot(xVals, estYVals, 'r',
               label = 'Linear fit, k = '
               + str(round(1/model[0], 5)))
    pylab.legend(loc = 'best')



def rSquared(observed, predicted):
    error = ((predicted - observed)**2).sum()
    meanError = error/len(observed)
    return 1 - (meanError/numpy.var(observed))

def genFits(xVals, yVals, degrees):
    models = []
    for d in degrees:
        model = pylab.polyfit(xVals, yVals, d)
        models.append(model)
    return models

def testFits(models, degrees, xVals, yVals, title):
    pylab.plot(xVals, yVals, 'o', label = 'Data')
    for i in range(len(models)):
        estYVals = pylab.polyval(models[i], xVals)
        error = rSquared(yVals, estYVals)
        pylab.plot(xVals, estYVals,
                   label = 'Fit of degree '\
                   + str(degrees[i])\
                   + ', R2 = ' + str(round(error, 5)))
    pylab.legend(loc = 'best')
    pylab.title(title)

######################################################

def genNoisyParabolicData(a, b, c, xVals, fName):
    '''2차 식에 노이즈 추가'''
    yVals = []

    for x in xVals:
        theoreticalVal = a*x**2 + b*x +c
        yVals.append(theoreticalVal + random.gauss(0, 35))

    f = open(fName, 'w')
    f.write('x y\n') 
    for i in range(len(yVals)):
        f.write(str(yVals[i]))+ ' ' + str(xVals[i] + '\n')
    f.close()

xVals = range(-10, 11, 1)
a, b, c = 3, 0, 0

genNoisyParabolicData(a, b, c, xVals, 'Mystery Data.txt')


# 2개의 데이터셋 관찰
degrees = (2, 4, 8, 16)

random.seed(0)
xVals1, yVals1 = getData("Dataset 1.txt")
models1 = genFits(xVals, yVals1, degrees)
testFits(models1, degrees, xVals1, yVals1, 'DataSet 1.txt')

pylab.figure()
xVals2, yVals2 = getData("Dataset 2.txt")
models2 = genFits(xVals, yVals1, degrees)
testFits(models1, degrees, xVals1, yVals1, 'DataSet 1.txt')

# 검증 코드
pylab.figure()
testFits(models1, degrees, xVals2, yVals2, "DataSet 2/Model 1")
pylab.figure()
testFits(models2, degrees, xVals1, yVals1, "DataSet 1/Model 2")

# 복잡도 증가시키기
xVals = (0, 1, 2, 3)
yVals = xVals
pylab.plot(xVals, yVals, label = "Actual values")

a, b, c = pylab.polyfit(xVals, yVals, 2)
print("a =", round(a, 4), 'b =', round(b, 4), 'c =', round(c, 4))

estYVals = pylab.polyval((a, b, c), xVals)
pylab.plot(xVals, estYVals, 'r--', label = "Predictive values")
print("R-squared =", rSquared(yVals, estYVals))

# 완벽한 데이터 추가
xVals = xVals + (20, )
yVals = xVals
pylab.plot(xVals, yVals, label = "Actual values")
estYVals = pylab.polyval((a, b, c), xVals)
pylab.plot(xVals, estYVals, 'r--', label = "Predictive values")
print("R-squared =", rSquared(yVals, estYVals))

# 노이즈 데이터 추가
xVals = (0, 1, 2, 3)
yVals = (0, 1, 2, 3.1)
pylab.plot(xVals, yVals, label = "Actual values")
model = pylab.polyfit(xVals, yVals, 2)
print(model)
estYVals = pylab.polyval(model, xVals)
pylab.plot(xVals, estYVals, 'r--', label = "Predicted values")
print("R-squared =", rSquared(yVals, estYVals))

# 같은 모델로 다른 점 예측
xVals = xVals + (20,)
yVals = xVals
estYVals = pylab.polyval(model, xVals)
print("R-squared =", rSquared(yVals, estYVals))
pylab.figure()
pylab.plot(xVals, estYVals)


## 최고 기온 변화 코드
class tempDatum(object):
    def __init__(self, s):
        info = s.split(',')
        self.high = float(info[1])
        self.year = int(info[2][0:4])
    
    def getHigh(self):
        return self.high
    
    def getYear(self):
        return self.year
    
def getTempData():
    inFile = open('temperatures.csv')
    data = []

    for l in inFile:
        data.append(tempDatum(l))

    return data
    
def getYearlyMeans(data):
    years = {}
    for d in data:
        try:
            years[d.getYear()].append(d.getHigh())
        except:
            years[d.getYear()] = [d.getHigh()]
        
    for y in years:
        years[y] = sum(years[y]) / len(years[y])
        
    return years

# 그래프로 표시
data = getTempData()
years = getYearlyMeans(data)
xVals, yVals = [], []

for e in years:
    xVals.append(e)
    yVals.append(years[e])
pylab.plot(xVals, yVals)
pylab.xlabel('Year')
pylab.ylabel('Mean Daily High (C)')
pylab.title('Select U.S. Cities')

numSubsets = 10
dimensions = (1, 2, 3, 4)
rSquares = {}
for d in dimensions:
    rSquares[d] = []

def splitData(xVals, yVals):
    toTrain = random.sample(range(len(xVals)), len(xVals) // 2)
    
    trainX, trainY, testX, testY = [], [], [], []

    for i in range(len(xVals)):
        if i in toTrain:
            trainX.append(xVals[i])
            trainY.append(yVals[i])
        else:
            testX.append(xVals[i])
            testY.append(yVals[i])
    
    return trainX, trainY, testX, testY

# 학습, 검증, 보고
for f in range(numSubsets):
    trainX, trainY, testX, testY = splitData(xVals, yVals)
    for d in dimensions:
        model = pylab.polyfit(trainX, trainY, d)
        estYVals = pylab.polyval(model, testX)
        rSquares[d].append(rSquared(testY, estYVals))

print("Mean R-squares for test data")
for d in dimensions:
    mean = round(sum(rSquares[d]) / len(rSquares[d]), 4)
    sd = round(numpy.std(rSquares[d]), 4)
    print('For dimensionality', d, 'mean =', mean, 'Std =', sd)