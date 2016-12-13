from neo4j.v1 import GraphDatabase, basic_auth

driver = GraphDatabase.driver("bolt://localhost", auth=basic_auth("neo4j", "neo4j1")) #i changed the default password :P
session = driver.session()

##session.run("MATCH (n) DETACH DELETE n")  #THIS INITIALISES/DELETES THE WHOLE DATABASE -- CAREFUL!!!
##session.run(
##"""
##CREATE (a:Movie {title:'Heat'})
##CREATE (b:Actor {name:'Al Pacino'})
##CREATE (c:Actor {name:"Robert De Niro"})
##CREATE (d:Director {name : "Michael Mann"})
##CREATE (e:Movie {title : "The Insider"})
##CREATE (f:Actor {name : "Russel Crowe"})
##
##CREATE (b)-[g:playedIn]->(a)
##CREATE (c)-[h:playedIn]->(a)
##CREATE (d)-[i:directed]->(a)
##CREATE (d)-[j:directed]->(e)
##CREATE (b)-[k:playedIn]->(e)
##CREATE (f)-[l:playedIn]->(e)
##""")

actorResults = session.run("""
MATCH (a:Actor)
RETURN a.name AS ActorName
""")

movieResults = session.run("""
MATCH (c:Movie)
RETURN c.title as MovieTitle
""")

directorResults = session.run("""
MATCH (b:Director)
RETURN b.name AS DirectorName
""")


edgeResults = session.run("""
MATCH (a)-[r]-(b)
RETURN a as Source, type(r) as Edge, b as Target
""")

for record in actorResults:
    print(record)

for record in directorResults:
    print(record)

for record in movieResults:
    print(record)

for record in edgeResults:
    print(record)
    
session.close()

