from parsimonious.grammar import Grammar
from algebra import getNodes, expandIn, expandOut
import toyGraph
import toyRelation

class Graphy(object):

    def __init__(self, env={}):
        self.env = env
        defaultEnf(self.env)
        
    def parse(self, source):
        grammar = self.grammarFromDocStr()
        return Grammar(grammar)['program'].parse(source)

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
        
    def program(self, node, children):
        'program = select _ "|" _ fromStatement (_ "|" _ whereStatement)?'
        specification , _, _ , _, relation, whereStatement = children

        if whereStatement:
            collumn, field, mustEqual = whereStatement[0][3]
            relation = selection(collumn, field, mustEqual, relation)
        #print("projecting",specification,"\n","from", relation)
        print(projection(specification, relation))
        return children

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
    env['getNodes'] = lambda argument: getNodes(argument,toyGraph.myGraph)
    env['expandIn'] = lambda source,target,relation: expandIn(source,target,relation,toyGraph.myGraph)
    env['expandOut'] = lambda x: "funcy says " + x
    
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
        if getattr(item[collumn], field) == mustEqual:
            newRelation.addRow(item)

    return newRelation

a = Graphy()
a.eval("select * | from expandIn(x,y,getNodes(x)) | where yx.label=playedIn")  
