from source.Parser.Earley import *


class Variable(object):
    def __init__(self, name=None, type_v=None):
        self.name = name
        self.type_v = type_v


class Function(object):
    def __init__(self, name=None, link=None, params=[]):
        self.name = name
        self.params = params
        self.link = link
        self.used = False


class FunctionStorage(object):
    def __init__(self):
        self.functions = list()

    def getFunction(self, node: TreeNode):
        for func in self.functions:
            if func.name == node.children[0].lexeme.lexeme:
                paramsCount = 0
                if len(node.children) > 1:
                    paramsCount += 1
                    tempParams = node.children[1].children
                    while len(tempParams) == 2:
                        paramsCount += 1
                        tempParams = tempParams[1].children
                if len(func.params) == paramsCount:
                    return func
        return None

    def optimizeUnused(self):
        for func in self.functions:
            if not func.used:
                func.link = None


class Optimizer(object):
    def __init__(self, tree, function_storage=FunctionStorage()):
        self.functionStorage = function_storage
        self.tree = tree.children[0]

    def add_function(self, node: TreeNode):
        newFunction = Function()
        newFunction.name = node.children[1].lexeme.lexeme
        newFunction.link = node
        if len(node.children) == 4:
            tempParam = node.children[2].children
            while len(tempParam) == 3:
                newFunction.params.append(Variable(tempParam[1].lexeme.lexeme, tempParam[0].lexeme.lexeme))
                tempParam = tempParam[2].children
            newFunction.params.append(Variable(tempParam[1].lexeme.lexeme, tempParam[0].lexeme.lexeme))
        self.functionStorage.functions.append(newFunction)

    def parse(self, node: TreeNode):
        if node.rule.name == '<объявление функции>':
            self.add_function(node)
        if node.rule.name == '<вызов функции>':
            if self.functionStorage.getFunction(node) is not None:
                self.functionStorage.getFunction(node).used = True
        if node.children:
            for nextNode in node.children:
                self.parse(nextNode)

    def optimize(self):
        self.parse(self.tree)
        self.functionStorage.optimizeUnused()
        print('jh')
