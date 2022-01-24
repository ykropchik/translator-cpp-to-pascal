from source.Parser.Earley import Node
from source.Lexer.ErrorTypes import ErrorTypeSemantic
from source.Semantic_Analyzer import ReservedWords


class Variable(object):
    def __init__(self, type_v, name):
        self.type_v = type_v,
        self.name = name,


class Function(object):
    def __init__(self, type_v, name, params):
        self.type_v = type_v,
        self.name = name,
        self.params = params


class VariableSemanticAnalyser:
    def __init__(self, tree):
        self.variables = [],
        self.tree = tree,
        self.file = None

    def findExpressionType(self, node: Node):
        for part in node.children:
            if part.value.name == '<число>':
                if part.value.production == '<целое число>':
                    return 'int'
                if part.value.production == '- <целое число>':
                    return 'int'
                if part.value.production == '<вещественное число>':
                    return 'float'
                if part.value.production == '- <вещественное число>':
                    return 'float'
            if part.value.name == '<булево выражение>':
                return 'bool'
            if part.value.name == '\'<буква>\'':
                return 'char'
            # if part.value.name == '<вызов функции>':
            #     return 'func'
        return ErrorTypeSemantic.UNFINISHED_EXPRESSION

    def findName(self, node: Node):
        if node.value.dot_index == 1:
            if node.value.production == '<начало имени>':
                for part in node.children:
                    return self.findName(part)
            if node.value.production == '<буква>':
                for part in node.children:
                    return self.findName(part)
            if node.value.name == '<буква>':
                return node.value.production
        elif node.value.dot_index == 2:
            for child in node.children:
                if child.value.name == '<продолжение имени>':
                    nameContinuation = None
                    for part in child.children:
                        nameContinuation += part.value.production
                    return nameContinuation

        return ErrorTypeSemantic.MISSING_VARIABLE_NAME

    def findType(self, node: Node):
        for part in node.children:
            if part.value.name == 'bool' or part.value.name == 'char' or part.value.name == 'short' or part.value.name == \
                    'unsigned short int' or part.value.name == 'int' or part.value.name == \
                    'short int' or part.value.name == 'unsigned short' or part.value.name == \
                    'unsigned int' or part.value.name == 'float' or part.value.name == 'double':
                return part.value.name
            return ErrorTypeSemantic.UNKNOWN_DATA_TYPE

    # TODO:: Проверить работу find-функций
    def addVariable(self, node: Node):  # Input: value = <инициализация переменной> || <объявление переменной> ||
        # <обновление переменной>
        newVariable = Variable(None, None)
        typeCheck = None
        errorCheck = None
        for part in node.children:
            if part.value.name == '<выражение>':
                typeCheck = self.findExpressionType(part)
            if part.value.name == '<имя переменной>':
                newVariable.name += self.findName(part)
            if part.value.name == '<тип данных>':
                newVariable.type_v = self.findType(part)
        if typeCheck and typeCheck != newVariable.type_v:
            print(ErrorTypeSemantic.TYPE_MISMATCH + newVariable.name)
            errorCheck = True
        if newVariable.name in ReservedWords.ReservedWords.data:
            print(ErrorTypeSemantic.USAGE_OF_RESERVED_IDENTIFIER + newVariable.name)
            errorCheck = True
        for variable in self.variables:
            if variable.name == newVariable.name:
                print(ErrorTypeSemantic.MULTIPLE_VARIABLE_DECLARATION + newVariable.name)
                errorCheck = True
        if errorCheck is None:
            # TODO: хз почему variables - это не list
            # Возможно PyCharm думает, что это обращение к атрибуту которого не существует.
            self.variables.append(newVariable)

    def updateVariableCheck(self, node: Node):  # Input: value = <обновление переменной>
        typeCheck = None
        nameCheck = None
        exist = None
        for part in node.children:
            if part.value.name == '<выражение>':
                typeCheck = self.findExpressionType(part)
            if part.value.name == '<имя переменной>':
                nameCheck = self.findName(part)
        for variable in self.variables:
            if variable.name == nameCheck:
                exist = True
                if variable.type_v != typeCheck:
                    print(ErrorTypeSemantic.TYPE_MISMATCH + nameCheck)
        if exist is None:
            print(ErrorTypeSemantic.UNDECLARED_VARIABLE + nameCheck)

    def parse(self, node):
        if node.value.name == '<инициализация переменной>' or node.value.name == '<объявление переменной>':
            self.addVariable(node)
        if node.value.name == '<обновление переменной>':
            self.updateVariableCheck(node)
        if not node.children:
            for nextNode in node.children:
                self.parse(nextNode)


class FunctionSemanticAnalyser:
    def __init__(self, tree, *functions: Function):
        self.tree = tree,
        self.functions = list(functions),
        self.file = None

    def parse(self):
        print(self.tree)
