class Node(object):
    '''각 노드를 하나의 객체로 보자'''
    def __init__(self, name):
        self.name = name
    
    def getName(self):
        return self.name
    
    def __str__(self):
        return self.name

class Edge(object):
    def __init__(self, src, dest):
        self.src = src
        self.dest = dest
    
    def getSource(self):
        return self.src
    
    def getDestination(self):
        return self.dest
    
    def __str__(self):
        return self.src.getName() + "->" + self.dest.getName()
    

class Digraph(object):
    '''유향그래프 구현하기'''
    def __init__(self):
        self.edges = {}
    
    def addNode(self, node):        # edge 딕셔너리의 key가 node가 된다.
        if node in self.edges:
            raise ValueError("Duplicate node")
        else:
            self.edges[node] = []
        
    def addEdge(self, edge):
        src = edge.getSource()
        dest = edge.getDestination()
        if not (src in self.edges and dest in self.edges):
            raise ValueError("Node not in graph")
        self.edges[src].append(dest)
    
    def childrenOf(self, node):
        return self.edges[node]
    
    def hasNode(self, node):
        return node in self.edges
    
    def getNode(self, name):
        for n in self.edges:
            if n.getName() == name:
                return n
        raise NameError(name)
    
    def __str__(self):
        result = ''
        for src in self.edges:
            for dest in self.edges[src]:
                result = result + src.getName() + "->" + dest.getName() + '\n'
        return result[:-1]

class Graph(Digraph):
    '''Digraph의 상속을 받는다'''
    def addEdge(self, edge):
        Digraph.addEdge(self, edge)
        rev = Edge(edge.getDestination(), edge.getSource())
        Digraph.addEdge(self, rev)


# 본격적으로 최단경로 문제 풀기
def buildCityGraph(graphType):
    '''유향그래프인지, 무향그래프인지를 입력받아 도시 그래프를 만든다.
    전혀 복잡하지 않다. 그냥 그래프에 Node와 Edge를 추가하는 것이다.'''
    g = graphType()

    for name in ('Boston', 'Providence', 'New York', 'Chicago', 'Denver', 'Phoenix', 'Los Angeles'):
        g.addNode(Edge(g.getNode("Boston"), g.getNode("Providence")))
        g.addNode(Edge(g.getNode("Boston"), g.getNode("New York")))
        g.addNode(Edge(g.getNode("Province"), g.getNode("Boston")))
        g.addNode(Edge(g.getNode("Province"), g.getNode("New York")))
        g.addNode(Edge(g.getNode("New York"), g.getNode("Chicago")))
        g.addNode(Edge(g.getNode("Chicago"), g.getNode("Denver")))
        g.addNode(Edge(g.getNode("Chicago"), g.getNode("Phoenix")))
        g.addNode(Edge(g.getNode("Denver"), g.getNode("Phoenix")))
        g.addNode(Edge(g.getNode("Denver"), g.getNode("New York")))
        g.addNode(Edge(g.getNode("Los Angeles"), g.getNode("Boston")))
    
    return g

def printPath(path):
    '''경로 출력 함수'''
    result = ''
    for i in range(len(path)):
        result = result + str(path[i])
        if i != len(path) - 1:
            result = result + '->'
    return result 

def DFS(graph, start, end, path, shortest, toPrint = False):        # toPrint는 출력 여부만 결정한다.
    [start]
    if toPrint:
        print("Current DFS path: ", printPath(path))
    if start == end:
        return path
    for node in graph.ChildrenOf(start):
        if node not in path:    # 무한 순환 방지(갔던 곳 다시 안 가도록)
            if shortest == None or len(path) < len(shortest):       # 지금 구한 게 최적이면
                newPath = DFS(graph, node, end, path, shortest, toPrint)

                if newPath != None:
                    shortest = newPath
        elif toPrint:
                print("Already Visited", node)
        
    return shortest

def shortestPath(graph, start, end, toPrint = False):
    return DFS(graph, start, end, [], Node, toPrint)

def testSP(source, destination):
    g = buildCityGraph(Digraph)
    sp = shortestPath(g, g.getNode(source), g.getNode(destination), toPrint=True)

    if sp != None:
        print("Shortest path from {} to {} is {}.".format(source, destination, printPath(sp)))
    else:
        print("There is no path from {} to {}.".format(source, destination))

testSP("Boston", "Chicago")

printQueue = True

def BFS(graph, start, end, toPrint = False):
    initPath = [start]
    pathQueue = [initPath]
    while len(pathQueue) != 0:
        if printQueue:
            print('Queue:', len(pathQueue))
            for p in pathQueue:
                print(printPath(p))
        tmpPath = pathQueue.pop(0)
        if toPrint:
            print('Current BFS path:', printPath(tmpPath))
            print()
        lastNode = tmpPath[-1]
        if lastNode == end:
            return tmpPath
        for nextNode in graph.childrenOf(lastNode):
            if nextNode not in tmpPath:
                newPath = tmpPath + [nextNode]
                pathQueue.append(newPath)
    return None

def shortestPath(graph, start, end, toPrint = False):
    return BFS(graph, start, end, toPrint)
    
testSP('Boston', 'Phoenix')
    
