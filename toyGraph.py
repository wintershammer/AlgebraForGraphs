

class Node: #represents nodes of the graph, which carry a dict of their attributes

    def __init__(self,label,dic):
        self.label = label
        self.dic = dic
        
    def __str__(self):
        return str(self.dic) #+ str(self.label)


class Edge: #represents directed edges - source and target are nodes - should i add a dict too?

    def __init__(self,label,source,target):
        self.label = label
        self.source = source
        self.target = target
        
    def __str__(self):
        return str(self.source) + "---" + str(self.label) + "-->" + str(self.target)


def findEdges(source,target,edges):
    listOfEdges = []
    for edge in edges:
        if edge.source == source and edge.target == target:
            listOfEdges.append(edge)
    return listOfEdges

def findOutGoingEdges(source,edges):
    listOfEdges = []
    for edge in edges:
        if edge.source == source:
            listOfEdges.append(edge)
    return listOfEdges

def findInGoingEdges(source,edges):
    listOfEdges = []
    for edge in edges:
        if edge.source == source:
            listOfEdges.append(edge)
    return listOfEdges

nodeOne = Node("movie",{"title" : "Heat"})
nodeTwo = Node("actor",{"name" : "Al Pacino"})
nodeThree = Node("actor",{"name" : "Robert De Niro"})
nodeFour = Node("director",{"name" : "Michael Mann"})
nodeFive = Node("movie",{"title": "The Insider"})
nodeSix = Node("actor",{"name" : "Russel Crowe"})

edgeOne = Edge("playedIn", nodeTwo, nodeOne)
edgeTwo = Edge("playedIn", nodeThree,nodeOne)
edgeThree = Edge("directed", nodeFour, nodeOne)
edgeFour = Edge("directed", nodeFour, nodeFive)
edgeFive = Edge("playedIn", nodeTwo, nodeFive)
edgeSix = Edge("playedIn", nodeSix, nodeFive)
edgeSeven = Edge("isSimilarTo", nodeOne, nodeFive)
edgeEight = Edge("isSimilarTo", nodeFive, nodeOne)

myGraph = [[nodeOne,nodeTwo,nodeThree,nodeFour,nodeFive,nodeSix],[edgeOne,edgeTwo,edgeThree,edgeFour,edgeFive,edgeSix,edgeSeven,edgeEight]]




