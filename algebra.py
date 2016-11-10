import toyGraph
import toyRelation
import copy



def getNodes(argument,graph):
    newRelation = toyRelation.Relation()
    for node in graph[0]:
        newRelation.addRow({argument : node})

    return newRelation

def expandOut(source,target,relation,graph):
    expandedRelation = relation
    for row in expandedRelation.getRows():
        if source in row:
            for edge in toyGraph.findOutGoingEdges(row[source],graph[1]):
                xyCollumn = source + target #the middle collumn in : X| XY | Y
                row[xyCollumn]  = edge
                row[target] = edge.target
                
    return expandedRelation
    

def expandIn(source,target,relation,graph):
    expandedRelation = toyRelation.Relation()
    for row in relation.getRows():
        if source in row:
            for edge in toyGraph.findInGoingEdges(row[source],graph[1]):
                xyCollumn = source + target #the middle collumn in : X| XY | Y
                expandedRelation.addRow({source : row[source], xyCollumn : edge, target : edge.target})
                
    return expandedRelation  

start = getNodes("x",toyGraph.myGraph)
print(start)

##TODO: make project into a proper operator that takes an argument and constraints
afterProjection = toyRelation.Relation()
for item in start.getRows():
    if item["x"].label == "actor":
        afterProjection.addRow(item)

print("-------------------")

afterExpansionOne = expandOut("x","y",afterProjection,toyGraph.myGraph)
print(afterExpansionOne)

