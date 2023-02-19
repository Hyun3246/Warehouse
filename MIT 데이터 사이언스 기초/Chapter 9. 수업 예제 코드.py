import pylab, numpy

def getData(fileName):
    '''수업 시간에 다루지 않음'''
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
    '''수업 시간에 다루지 않음'''
    pylab.title('Measured Displacement of Spring')
    pylab.xlabel('|Force| (Newtons)')
    pylab.ylabel('Distance (meters)')

def plotData(fileName):
    xVals, yVals = getData(fileName)
    xVals = pylab.array(yVals)
    xVals = xVals * 9.81
    pylab.plot(xVals, yVals, 'bo', label = "Measured displacements")
    labelPlot()

def fitData(fileName):
    '''추세선 그리기. polyfit 사용'''
    xVals, yVals = getData(fileName)
    xVals = pylab.array(xVals)
    yVals = pylab.array(yVals)
    xVals = xVals * 9.81

    pylab.plot(xVals, yVals, 'bo', label = "Measured points")
    labelPlot()

    a, b = pylab.polyfit(xVals, yVals, 1)
    estYVals = a * pylab.array(xVals) + b
    print('a =', a, 'b =', b)
    pylab.plot(xVals, estYVals, 'r', label = "Linear fit, k =" + str(round(1/a, 5)))

    pylab.legend(loc = 'best')

def fitData1(fileName):
    '''추세선 그리기. polyval 사용'''
    xVals, yVals = getData(fileName)
    xVals = pylab.array(xVals)
    yVals = pylab.array(yVals)
    xVals = xVals * 9.81

    pylab.plot(xVals, yVals, 'bo', label = "Measured points")

    labelPlot()

    model = pylab.polyfit(xVals, yVals, 1)
    estYVals = pylab.polyval(model, xVals)
    pylab.plot(xVals, estYVals, 'r', label = "Linear fit k =" + str(round(1/model[0], 5)))
    pylab.legend(loc = 'best')

def aveMeanSquareError(data, predicted):
    '''평균제곱오차 계산'''
    error = 0.0

    for i in range(len(data)):
        error += (data[i] - predicted[i]) ** 2
    return error/len(data)

def rSquared(observed, predicted):
    '''결정계수 계산'''
    error = ((predicted - observed) ** 2).sum()
    meanError = error / len(observed)

    return 1- (meanError / numpy.var(observed))

def getFits(xVals, yVals, degrees):
    '''여러 차수로 fitting 하는 함수'''
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
        pylab.plot(xVals, estYVals, label = 'Fit of degree' + str(degrees[i]) + ', R2 =' + str(round(error, 5)))
    pylab.legend(loc = 'best')
    pylab.title(title)