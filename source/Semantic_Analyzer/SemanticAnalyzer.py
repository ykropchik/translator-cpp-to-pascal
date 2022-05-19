from source.Parser.Earley import Node
from source.Lexer.ErrorTypes import ErrorTypeSemantic
from source.Semantic_Analyzer import ReservedWords


class Variable(object):
    def __init__(self, type_v, name):
        self.type_v = type_v,
        self.name = name


class VariableStorage(object):
    def __init__(self):
        self.variables = list()
        self.children = list()
        self.parent = None

    def addChildren(self):
        var_s = VariableStorage()
        self.children.append(var_s)
        var_s.parent = self
        return var_s

    def addVariable(self, var: Variable):
        self.variables.append(var)

    def exist(self, name, scope):
        while scope is not None:
            for value in scope.variables:
                if value.name == name:
                    return True
            scope = scope.parent
        return False

    def getVariable(self, name, scope):
        while scope is not None:
            for value in scope.variables:
                if value.name == name:
                    return value
            scope = scope.parent
        return None


class Function(object):
    def __init__(self, type_v, name, params):
        self.type_v = type_v,
        self.name = name,
        self.params = params


class SemanticError:
    def __init__(self, line, name, error_name):
        self.errorName = error_name
        self.line = line
        self.name = name
        self.assumptions = set()

    def addAssumption(self, assumption):
        self.assumptions.add(assumption)

    def __str__(self):
        return "{0} | Error: {1} \"{2}\"" \
            .format(self.line, self.errorName, self.name)


class VariableSemanticAnalyser:
    def __init__(self, tree):
        self.tree = tree
        self.functions = []
        self.file = None

    def findExpressionType(self, node: Node):
        if node.lexeme and node.lexeme.lexemeType.name == 'INT_NUMBER':
            return ['int']
        elif node.lexeme and node.lexeme.lexemeType.name == 'REAL_NUMBER':
            return ['double', 'float']
        elif node.lexeme and node.lexeme.lexemeType.name == 'CHAR_DATA':
            return ['char']
        elif node.lexeme and node.lexeme.lexemeType.name == 'STRING_DATA':
            return ['string']
        else:
            return ['int']

    def addVariable(self, node: Node, scope: VariableStorage):
        newVariable = Variable(None, None)
        typeCheck = None
        errorCheck = None
        for part in node.children:
            if part.rule.name == '<тип данных>':
                newVariable.type_v = part.lexeme.lexeme
            if part.rule.name == '<имя переменной>':
                newVariable.name = part.lexeme.lexeme
            if part.rule.name == '<выражение>':
                typeCheck = self.findExpressionType(part)
        if typeCheck and newVariable.type_v not in typeCheck and newVariable.name[0] is not None:
            print(SemanticError(node.lexeme.lineNumber, newVariable.name,
                                ErrorTypeSemantic.TYPE_MISMATCH.value))
            errorCheck = True
        if newVariable.name in ReservedWords.ReservedWords.data and newVariable.name[0] is not None:
            print(SemanticError(node.lexeme.lineNumber, newVariable.name,
                                ErrorTypeSemantic.USAGE_OF_RESERVED_IDENTIFIER.value))
            errorCheck = True
        if scope.exist(newVariable.name, scope):
            print(SemanticError(node.lexeme.lineNumber, newVariable.name,
                                ErrorTypeSemantic.MULTIPLE_VARIABLE_DECLARATION.value))
            errorCheck = True
        if errorCheck is None:
            scope.addVariable(newVariable)

    def updateVariableCheck(self, node: Node, scope: VariableStorage):
        typeCheck = None
        nameCheck = ''
        for part in node.children:
            if part.rule.name == '<имя переменной>':
                nameCheck = part.lexeme.lexeme
            if part.rule.name == '<выражение>':
                typeCheck = self.findExpressionType(part)
            if part.rule.name == '<унарный алгебраический оператор>':
                typeCheck = ['int']
        if not scope.exist(nameCheck, scope):
            print(SemanticError(node.lexeme.lineNumber, nameCheck, ErrorTypeSemantic.UNDECLARED_VARIABLE.value))
        else:
            var = scope.getVariable(nameCheck, scope)
            if var.type_v not in typeCheck:
                print(SemanticError(node.lexeme.lineNumber, nameCheck, ErrorTypeSemantic.TYPE_MISMATCH.value))

    def addFunction(self, node: Node):
        newFunction = Function(None, None, None)
        for part in node.children:
            if part.rule.name == '<тип данных>':
                newFunction.type_v = part.lexeme.lexeme
            if part.rule.name == '<имя переменной>':
                newFunction.name = part.lexeme.lexeme

    def parse(self, node, scope: VariableStorage):
        newScope = scope
        if node.rule.name == '<инициализация переменной>':
            self.addVariable(node, scope)
        if node.rule.name == '<обновление переменной>':
            self.updateVariableCheck(node, scope)
        if node.rule.name == '<цикл for>':
            newScope = scope.addChildren()
        if node.rule.name == '<цикл while>':
            newScope = scope.addChildren()
        if node.rule.name == '<объявление функции>':
            self.addFunction(node)
            newScope = scope.addChildren()
        if node.rule.name == '<главная функция>':
            newScope = scope.addChildren()
        if node.children:
            for nextNode in node.children:
                self.parse(nextNode, newScope)