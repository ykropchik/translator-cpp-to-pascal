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

    def addVariable(self, node: Node):  # Input: value = <инициализация переменной> || <объявление переменной>
        newVariable = Variable(None, None)
        typeCheck = None
        errorCheck = None
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
            errorCheck = True
        reservedWords = []  # TODO: найти/объявить все зарезервированные слова
        if newVariable.name in reservedWords:
            # TODO: добовить в типы ошибок enum с семантическими ошибками. Добавить ошибку использование
            #  зарезервированного слова
            print("Error")
            errorCheck = True
        for variable in self.variables:
            if variable.name == newVariable.name:
                # TODO: добовить в типы ошибок enum с семантическими ошибками. Добавить ошибку многократного
                #  объявления переменной в области видимости
                print("Error")
                errorCheck = True
        if errorCheck is None:
            # TODO: хз почему variables - это не list
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
                    # TODO: добовить в типы ошибок enum с семантическими ошибками. Добавить ошибку несоответствия типов
                    print('Error')
        if exist is None:
            # TODO: добовить в типы ошибок enum с семантическими ошибками. Добавить ошибку не существования переменной
            print('Error')

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
