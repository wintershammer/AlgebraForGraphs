from neo4j.v1 import GraphDatabase, basic_auth
import toyGraph


def getNodeById(nodeList,iden):
    for node in nodeList:
        if node.iden == iden:
            return node
        
driver = GraphDatabase.driver("bolt://localhost", auth=basic_auth("yourAuthHere", "yourKeyHere")) #i changed the default password :P
session = driver.session()

allNodes = session.run("""
MATCH (a)
RETURN (a)
""")

allEdges = session.run("""
MATCH (a)-[r]->(b)
RETURN a as Source, r as Edge, b as Target
""")

edges = []
nodes = []

for item in allNodes:
    #newNode = toyGraph.Node()
    label = list((item["a"].labels))
    nodes.append(toyGraph.Node(label[0],item["a"].properties,item["a"].id))
    
for item in allEdges:
    sourceNode = getNodeById(nodes,item["Source"].id)
    targetNode = getNodeById(nodes,item["Target"].id)
    edgeLabel = item["Edge"].type
    edges.append(toyGraph.Edge(edgeLabel,sourceNode,targetNode,item["Edge"].id))
        
        

##for item in nodes:
##    print(item)
##print("--------")
##for item in edges:
##    print(item)
    
session.close()


myGraph = myGraph = [nodes,edges]

