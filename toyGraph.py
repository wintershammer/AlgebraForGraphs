

class Node: #represents nodes of the graph, which carry a dict of their attributes

    def __init__(self,label,dic,iden):
        self.label = label
        self.dic = dic
        self.iden = iden 
        
    def __str__(self):
        return str(self.dic) #+ " " + str(self.label) + " " + str(self.iden)


class Edge: #represents directed edges - source and target are nodes - should i add a dict too?

    def __init__(self,label,source,target, iden):
        self.label = label
        self.source = source
        self.target = target
        self.iden = iden
        
    def __str__(self):
        return str(self.source) + "---" + str(self.label) + "-->" + str(self.target)


def findEdges(source,target,edges):
    listOfEdges = []
    for edge in edges:
        if edge.source == source and edge.target == target:
            listOfEdges.append(edge)
    return listOfEdges

def findOutGoingEdges(source,edges): #source is the source node, edges is the list of all edges
    listOfEdges = []
    for edge in edges:
        if edge.source == source:
            listOfEdges.append(edge)
    return listOfEdges

def findInGoingEdges(target,edges):
    listOfEdges = []
    for edge in edges:
        if edge.target == target:
            listOfEdges.append(edge)
    return listOfEdges

nodeOne = Node("movie",{"title" : "Heat"},0)
nodeTwo = Node("actor",{"name" : "Al Pacino"},1)
nodeThree = Node("actor",{"name" : "Robert De Niro"},2)
nodeFour = Node("director",{"name" : "Michael Mann"},3)
nodeFive = Node("movie",{"title": "The Insider"},4)
nodeSix = Node("actor",{"name" : "Russel Crowe"},5)

edgeOne = Edge("playedIn", nodeTwo, nodeOne,0)
edgeTwo = Edge("playedIn", nodeThree,nodeOne,1)
edgeThree = Edge("directed", nodeFour, nodeOne,2)
edgeFour = Edge("directed", nodeFour, nodeFive,3)
edgeFive = Edge("playedIn", nodeTwo, nodeFive,4)
edgeSix = Edge("playedIn", nodeSix, nodeFive,5)
edgeSeven = Edge("isSimilarTo", nodeOne, nodeFive,6)
edgeEight = Edge("isSimilarTo", nodeFive, nodeOne,7)

myGraph = [[nodeOne,nodeTwo,nodeThree,nodeFour,nodeFive,nodeSix],[edgeOne,edgeTwo,edgeThree,edgeFour,edgeFive,edgeSix]]




