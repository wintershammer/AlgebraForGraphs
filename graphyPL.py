from parsimonious.grammar import Grammar
from algebra import getNodes, expandIn, expandOut
import toyGraph
import toyRelation
import connector
from collections import defaultdict

def hashJoin(table1,table2,index1,index2):
    h = defaultdict(list)
    # hash phase
    for s in table1.getRows():
        h[s[index1].iden].append(s)

    newRelation = toyRelation.Relation()

    for r in table2.getRows():
        for s in (h[r[index2].iden]):
            r.update(s)
            newRelation.addRow(r)
            
    return newRelation       

    
class Graphy(object):

    def __init__(self, env={}):
        self.env = env
        defaultEnf(self.env)
        
    def parse(self, source):
        grammar = self.grammarFromDocStr()
        return Grammar(grammar)['query'].parse(source)

    def eval(self, source):
        node = self.parse(source) if isinstance(source, str) else source
        method = getattr(self, node.expr_name, lambda node, children: children)
        if node.expr_name in ['ifelse', 'func']:
            return method(node)
        return method(node, [self.eval(n) for n in node])

    def grammarFromDocStr(self):
        #concat docstrings to generate grammar. careful: only visitor methods must have docstrings, and these must be grammar rules
        grammar = '\n'.join(v.__doc__ for k, v in vars(self.__class__).items()
                          if '__' not in k and hasattr(v, '__doc__') and v.__doc__)
        return grammar

    def query(self,node,children):
        'query = program / joinedProgram'
        return children

        
    def joinedProgram(self,node,children):
        'joinedProgram = "(" program ")" _ "JOIN" _ "(" program ")" _ "ON" _ stringLit "," _ stringLit'
        _,programOne,_,_,_,_,_,programTwo,_,_,_,_,attributeOne,_,_,attributeTwo = children
        resultsOne = programOne
        resultsTwo = programTwo
        return hashJoin(resultsOne,resultsTwo,attributeOne,attributeTwo)

        
    def program(self, node, children):
        'program = select _ "|" _ fromStatement (_ "|" _ whereStatement)?'
        specification , _, _ , _, relation, whereStatement = children

        if whereStatement:
            collumn, field, mustEqual = whereStatement[0][3]
            relation = selection(collumn, field, mustEqual, relation)
        #print("projecting",specification,"\n","from", relation)
        results = projection(specification, relation)
        return results

    def select(self, node, children):
        'select = "select" _ stringLit'
        _, _, arguments = children
        return arguments

    def fromStatement(self, node, children):
        'fromStatement = "from" _ call'
        _, _, results = children
        return results

    def whereStatement(self, node, children):
        'whereStatement = "where" _ stringLit "." stringLit "=" stringLit'
        _, _, collumn, _, attribute, _, value = children
        return (collumn,attribute,value)

        
    def call(self, node, children): 
        'call = name "(" callExpr ((sep callExpr)*)? ")"'
        name, _, argument1, arguments, _= children
        funName = (node.text.split("(")[0])
        returner = []
        returner.append(argument1)
        for item in arguments[0]:
            returner.append(item[1])
        return name(*returner)

    def callExpr(self, node, children): 
        'callExpr = call / stringLit'
        return children[0]

    def sep(self,node,children):
        'sep = _ "," _ '

    def name(self, node, children): #make that 'name = ~"[a-z0-9]+" _' if you want variable/func names to have alphanumeric instead
        'name = ~"[a-zA-Z]+"'
        return self.env.get(node.text.strip(), -1)
    
    def stringLit(self, node, children):
        'stringLit = ~"[a-z A-Z 0-9 ! # $ ? *]*" '
        return str(node.text)

    def _(self, node, children):
        '_ = ~"\s*"'

def defaultEnf(env):
    env['funcy'] = lambda x: "funcy says " + x
    env['funcyTwo'] = lambda x,y: "funcy2 says " + x + y 
    env['getNodes'] = lambda argument: getNodes(argument,connector.myGraph)
    env['expandIn'] = lambda source,target,relation: expandIn(source,target,relation,connector.myGraph)
    env['expandOut'] = lambda source,target,relation: expandOut(source,target,relation,connector.myGraph)
    
def projection(attribute, data): #attribute retains a trailing whitespace, gotta fix 
    newRelation = toyRelation.Relation()
    attribute = attribute[:-1] #[:-1] for trailing whitespace
    if attribute != "*":
        for row in data.getRows():
            #print(row[attribute])
            newRelation.addRow({attribute : row[attribute]})
    else:
        newRelation = data
    return newRelation

def selection(collumn, field, mustEqual, data):
    newRelation = toyRelation.Relation()
    for item in data.getRows():
        if(field in item[collumn].dic):
            if (item[collumn].dic[field] == mustEqual):
                newRelation.addRow(item)

    return newRelation
    
    

a = Graphy()
res = a.eval(
"select * | from expandOut(x,y,getNodes(x)) | where x.name=Robert De Niro"
)
print(res[0])
print("-------")
res = a.eval(
"select * | from expandOut(x,y,getNodes(x)) | where x.name=Al Pacino"
)
print(res[0])
print("-------")
res = a.eval(
"(select * | from expandOut(x,y,getNodes(x)) | where x.name=Al Pacino)" +
" JOIN " +
"(select * | from expandOut(a,b,getNodes(a)) | where a.name=Robert De Niro)" +
" ON y,b"
)
print(res[0])
print("-------")
