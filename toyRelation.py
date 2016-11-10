from toyGraph import *

class Relation(object):
    
    def __init__(self):
        self.rows =  []# list of row objects

    def addRow(self, row):
        self.rows.append(row)

    def getRows(self):
        return self.rows

    def __str__(self):
        string = ""
        for row in self.rows:
            for item in row:
                string += item + "=" + str(row[item]) + " "
            string += "\n"
        return string


##exampleTable = Relation()
##exampleTable.addRow({'x': nodeOne,'y': nodeTwo})
##exampleTable.addRow({'x': nodeThree,'y': nodeFour})
##
##print(exampleTable)
