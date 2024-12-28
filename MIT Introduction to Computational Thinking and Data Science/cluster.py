import pylab

#set line width
pylab.rcParams['lines.linewidth'] = 6
#set general font size 
pylab.rcParams['font.size'] = 12
#set font size for labels on axes
pylab.rcParams['axes.labelsize'] = 18
#set size of numbers on x-axis
pylab.rcParams['xtick.major.size'] = 5
#set size of numbers on y-axis
pylab.rcParams['ytick.major.size'] = 5
#set size of markers
pylab.rcParams['lines.markersize'] = 10

def minkowskiDist(v1, v2, p):
    '''p=1 맨해턴 거리, p=2 유클리드 거리'''
    dist = 0
    for i in range(len(v1)):
        dist += abs(v1[i] - v2[i])**p
    return dist**(1/p)

class Example(object):
    
    def __init__(self, name, features, label = None):
        self.name = name
        self.features = features
        self.label = label
        
    def dimensionality(self):
        return len(self.features)
    
    def getFeatures(self):
        return self.features[:]
    
    def getLabel(self):
        return self.label
    
    def getName(self):
        return self.name
    
    def distance(self, other):
        '''유클리드 거리 구하기'''
        return minkowskiDist(self.features, other.getFeatures(), 2)
    
    def __str__(self):
        return self.name +':'+ str(self.features) + ':' + str(self.label)

class Cluster(object):
    
    def __init__(self, examples):
        """Example은 비어있지 않은 Example 객체의 리스트"""
        self.examples = examples
        self.centroid = self.computeCentroid()
        
    def update(self, examples):
        oldCentroid = self.centroid
        self.examples = examples
        self.centroid = self.computeCentroid()
        return oldCentroid.distance(self.centroid)
    
    def computeCentroid(self):
        vals = pylab.array([0.0]*self.examples[0].dimensionality())
        for e in self.examples:
            vals += e.getFeatures()
        centroid = Example('centroid', vals/len(self.examples))
        return centroid

    def getCentroid(self):
        return self.centroid

    def variability(self):
        totDist = 0
        for e in self.examples:
            totDist += (e.distance(self.centroid))**2
        return totDist
        
    def members(self):
        for e in self.examples:
            yield e

    def __str__(self):
        names = []
        for e in self.examples:
            names.append(e.getName())
        names.sort()
        result = 'Cluster with centroid ' + str(self.centroid.getFeatures()) + ' contains:\n  '
        for e in names:
            result = result + e + ', '
        return result[:-2]  
        
def dissimilarity(clusters):
    """dissimilarity 계산"""
    totDist = 0
    for c in clusters:
        totDist += c.variability()
    return totDist
