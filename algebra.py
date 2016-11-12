import toyGraph
import toyRelation
import copy



def getNodes(argument,graph):
    newRelation = toyRelation.Relation()
    for node in graph[0]:
        newRelation.addRow({argument : node})

    return newRelation

def expandOut(source,target,relation,graph):
    newRelation = toyRelation.Relation()
    for row in relation.getRows():
        if source in row:
            for edge in toyGraph.findOutGoingEdges(row[source],graph[1]):
                newRow = copy.deepcopy(row)
                xyCollumn = source + target #the middle collumn in : X| XY | Y
                newRow[xyCollumn]  = edge
                newRow[target] = edge.target
                newRelation.addRow(newRow)
                
    return newRelation
    

def expandIn(target,source,relation,graph):
    newRelation = toyRelation.Relation()
    for row in relation.getRows():
        if target in row:
            for edge in toyGraph.findInGoingEdges(row[target],graph[1]):
                newRow = copy.deepcopy(row)
                yxCollumn = source + target #the middle collumn in : X| YX | Y
                newRow[yxCollumn]  = edge
                newRow[source] = edge.source
                newRelation.addRow(newRow)
                
    return newRelation

start = getNodes("x",toyGraph.myGraph)
print("---step 1: select all---")
print(start)

##TODO: make project into a proper operator that takes an argument and constraints
afterProjection = toyRelation.Relation()
for item in start.getRows():
    if item["x"].label == "actor" and item["x"].dic["name"] == "Al Pacino":
        afterProjection.addRow(item)

print("---step 2: project Al Pacino node---")
print(afterProjection)


afterExpansionOne = expandOut("x","y",afterProjection,toyGraph.myGraph)
print("---step 3: apply expandOut---")
print(afterExpansionOne)

afterExpansionTwo = expandIn("y","z",afterExpansionOne,toyGraph.myGraph)
print("---step 4: apply expandIn---")
print(afterExpansionTwo)
