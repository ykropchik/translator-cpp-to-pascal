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
    def __init__(self, tree, *variables: Variable):
        self.variables = list(variables),
        self.tree = tree,
        self.file = None

    def findExpressionType(self, node: Node):
        for part in node.children:
            if part.state.name == '<число>':
                if part.state.production.terms[0].name == '<целое число>':
                    return 'int'
                if part.state.production.terms[0].name == '- <целое число>':
                    return 'int'
                if part.state.production.terms[0].name == '<вещественное число>':
                    return 'float'
                if part.state.production.terms[0].name == '- <вещественное число>':
                    return 'float'
            if part.state.name == '<булево выражение>':
                return 'bool'
            if part.state.name == '\'<буква>\'':
                return 'char'
            # if part.value.name == '<вызов функции>':
            #     return 'func'
        return None

    def findName(self, node: Node):
        if node.state.dot_index == 1:
            if hasattr(node.state.production.terms[0], 'name') and node.state.production.terms[0].name == '<начало имени>':
                for part in node.children:
                    return self.findName(part)
            if hasattr(node.state.production.terms[0], 'name') and node.state.production.terms[0].name == '<буква>':
                for part in node.children:
                    return self.findName(part)
            if node.state.name == '<буква>':
                return node.state.production.terms[0]
        elif node.state.dot_index == 2:
            for child in node.children:
                if child.state.name == '<продолжение имени>':
                    nameContinuation = ''
                    for part in child.children:
                        nameContinuation += part.state.production.terms[0]
                    return nameContinuation

        return None

    def findType(self, node: Node):
        for part in node.children:
            if part.state.name == 'bool' or part.state.name == 'char' or part.state.name == 'short' or part.state.name == \
                    'unsigned short int' or part.state.name == 'int' or part.state.name == \
                    'short int' or part.state.name == 'unsigned short' or part.state.name == \
                    'unsigned int' or part.state.name == 'float' or part.state.name == 'double':
                return part.state.name
            return None

    # TODO:: Проверить работу find-функций
    def addVariable(self, node: Node):  # Input: value = <инициализация переменной> || <объявление переменной> ||
        # <обновление переменной>
        newVariable = Variable(None, None)
        typeCheck = None
        errorCheck = None
        for part in node.children:
            if part.state.name == '<выражение>':
                typeCheck = self.findExpressionType(part)
            if part.state.name == '<имя переменной>':
                newVariable.name = self.findName(part)
            if part.state.name == '<тип данных>':
                newVariable.type_v = self.findType(part)
        if typeCheck and typeCheck != newVariable.type_v and newVariable.name[0] is not None:
            print(ErrorTypeSemantic.TYPE_MISMATCH.value + newVariable.name[0])
            errorCheck = True
        if newVariable.name in ReservedWords.ReservedWords.data and newVariable.name[0] is not None:
            print(ErrorTypeSemantic.USAGE_OF_RESERVED_IDENTIFIER.value + newVariable.name[0])
            errorCheck = True
        for variable in self.variables[0]:
            if variable.name == newVariable.name:
                print(ErrorTypeSemantic.MULTIPLE_VARIABLE_DECLARATION.value + newVariable.name)
                errorCheck = True
        if errorCheck is None:
            # TODO: хз почему variables - это не list
            # Возможно PyCharm думает, что это обращение к атрибуту которого не существует.
            self.variables[0].append(newVariable)

    def updateVariableCheck(self, node: Node):  # Input: value = <обновление переменной>
        typeCheck = None
        nameCheck = ''
        exist = None
        for part in node.children:
            if part.state.name == '<выражение>':
                typeCheck = self.findExpressionType(part)
            if part.state.name == '<имя переменной>':
                nameCheck += self.findName(part)
        for variable in self.variables[0]:
            if variable.name == nameCheck:
                exist = True
                if variable.type_v != typeCheck:
                    print(ErrorTypeSemantic.TYPE_MISMATCH.value + nameCheck)
        if exist is None:
            print(ErrorTypeSemantic.UNDECLARED_VARIABLE.value + ' ' + nameCheck)

    def parse(self, node):
        if node.state.name == '<инициализация переменной>' or node.state.name == '<объявление переменной>':
            self.addVariable(node)
        if node.state.name == '<обновление переменной>':
            self.updateVariableCheck(node)
        if node.children:
            for nextNode in node.children:
                self.parse(nextNode)


class FunctionSemanticAnalyser:
    def __init__(self, tree, *functions: Function):
        self.tree = tree,
        self.functions = list(functions),
        self.file = None

    def parse(self):
        print(self.tree)
