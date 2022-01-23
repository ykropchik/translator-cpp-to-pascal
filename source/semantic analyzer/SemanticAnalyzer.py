from source.Parser.Earley import Node

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
        # TODO: Исходя из ноды <выражение> -> <ТИП> найти и вернуть тип в виде: int, char, strung...
        return 0

    def findName(self, node: Node):
        # TODO: Исходя из ноды <имя переменной> -> <НАЧАЛО ИМЕНИ><ПРОДОЛЖЕНИЕ ИМЕНИ> найти и вернуть имя переменной
        return 0

    def findType(self, node: Node):
        # TODO: Исходя из ноды <тип данных> -> bool|char|short найти и вернуть тип данных
        return 0

    def addVariableHelper(self, node: Node):
        newVariable = Variable(None, None)
        typeCheck = None
        for part in node.children:
            if part.value.name == '<выражение>':
                typeCheck = self.findExpressionType(part)
            if part.value.name == '<имя переменной>':
                newVariable.name = self.findName(part)
            if part.value.name == '<тип данных>':
                newVariable.type_v = self.findType(part)
        if typeCheck and typeCheck != newVariable.type_v:
            # TODO: добовить в типы ошибок enum с семантическими ошибками. Добавить ошибку несоответствия типов
            print("Error")
        else:
            # TODO: хз почему variables - это не list
            self.variables.append(newVariable)

    def parse(self):
        print(self.tree)


class FunctionSemanticAnalyser:
    def __init__(self, tree, *functions: Function):
        self.tree = tree,
        self.functions = list(functions),
        self.file = None

    def parse(self):
        print(self.tree)
