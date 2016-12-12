from parsimonious.grammar import Grammar
from algebra import getNodes, expandIn, expandOut
from toyGraph import myGraph

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
        'program = select _ "|" _ fromStatement'
        projection , _, _ , _, fromection = children
        print("projecting",projection,"\n","from", fromection)
        return children

    def select(self, node, children):
        'select = "select" _ stringLit'
        _, _, arguments = children
        return arguments

    def fromStatement(self, node, children):
        'fromStatement = "from" _ call'
        _, _, results = children
        return results
    
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
        'stringLit = ~"[a-z A-Z 0-9 ! # $ ?]*" '
        return str(node.text)

    def _(self, node, children):
        '_ = ~"\s*"'

def defaultEnf(env):
    env['funcy'] = lambda x: "funcy says " + x
    env['funcyTwo'] = lambda x,y: "funcy2 says " + x + y 
    env['getNodes'] = lambda argument: getNodes(argument,myGraph)
    env['expandIn'] = lambda source,target,relation: expandIn(source,target,relation,myGraph)
    env['expandOut'] = lambda x: "funcy says " + x
    
def projection(data, specification):
    returner = []
    for item in data:
        if data.label == specification:
            returner.append(item)
    return returner


a = Graphy()
a.eval("select kekus | from expandIn(x,y,getNodes(x))")  
