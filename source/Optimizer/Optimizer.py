from source.Parser.Earley import *
from source.Semantic_Analyzer.SemanticAnalyzer import VariableStorage


class LexemeArrayType(object):
    def __init__(self, lexeme, lexeme_type, line_number):
        self.lexeme = lexeme
        self.lexemeType = lexeme_type
        self.lineNumber = line_number


class Variable(object):
    def __init__(self, name=None, exp_link=None):
        self.name = name
        self.exp_link = exp_link


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
                func.link = None  # TODO: удалить из дерева ноду по ссылке link


class Optimizer(object):
    def __init__(self, tree, rules, function_storage=FunctionStorage(), variable_storage=VariableStorage()):
        self.functionStorage = function_storage
        self.variableStorage = variable_storage
        self.tree = tree.children[0]
        self.rules = rules

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

    def addVariable(self, node: TreeNode, scope: VariableStorage):
        newVariable = Variable()
        newVariable.name = node.children[1].lexeme.lexeme
        newVariable.exp_link = node.children[2].children[0]
        scope.addVariable(newVariable)

    def updateVariable(self, node: TreeNode, scope: VariableStorage):
        if scope.localExist(node.children[0].lexeme.lexeme, scope):
            var = scope.localExist(node.children[0].lexeme.lexeme, scope)
            upd = node.children[1].children[0]
            if var.exp_link.rule.name == '<алгебраическое выражение>' and upd.rule.name == '<алгебраическое выражение>':
                nodePlus = TreeNode(Rule(self.rules[43].name),
                                    LexemeArrayType('+', LexemeType.PLUS, var.exp_link.lexeme.lineNumber))
                endOfVar = var.exp_link.children
                while len(endOfVar) == 3:
                    endOfVar = endOfVar[2].children
                endOfVar.append(nodePlus)
                endOfVar.append(upd)
                node = None  # TODO: удалить из дерева ноду node

    def parse(self, node: TreeNode, scope: VariableStorage):
        newScope = scope
        if node.rule.name == '<инициализация переменной>':
            self.addVariable(node, scope)
        if node.rule.name == '<обновление переменной>':
            self.updateVariable(node, scope)
        if node.rule.name == '<объявление функции>':
            newScope = newScope.addChildren()
            self.add_function(node)
        if node.rule.name == '<цикл for>':
            newScope = scope.addChildren()
        if node.rule.name == '<цикл while>':
            newScope = scope.addChildren()
        if node.rule.name == '<главная функция>':
            newScope = scope.addChildren()
        if node.rule.name == '<вызов функции>':
            if self.functionStorage.getFunction(node) is not None:
                self.functionStorage.getFunction(node).used = True
        if node.children:
            for nextNode in node.children:
                self.parse(nextNode, newScope)

    def optimize(self):
        self.parse(self.tree, self.variableStorage)
        self.functionStorage.optimizeUnused()
        print('jh')
