# from enum import Enum
# INDENT = " " * 4
#
#
# class FuncNode(object):
#     def __init__(self):
#         self.name = None
#         self.params = []
#         self.body = []
#
# class Generator(object):
#     def __init__(self, tree):
#         if tree.rule.name != 'GAMMA':
#             raise ValueError
#         self.tree = tree.children[0]
#         self.resultTree =
#
#     def __getFuncName(self, treeNode):
#         return treeNode.children[0].lexeme.lexeme
#
#     def __generateFunc(self, treeNode):
#         result = ''
#         return result
#
#     def __generateProc(self, treeNode):
#         result = ''
#         return result
#
#     def __generateFunCall(self, treeNode):
#         return
#
#     def __generateMain(self, treeNode):
#         result = 'begin\n'
#         result += self.__generate_Helper(treeNode.children[0], 1)
#         return result + 'end.\n'
#
#     def __generateVar(self, treeNode):
#         if treeNode.rule.name == '<обновление переменной>':
#             result += self.__generateUpdateVar(treeNode)
#         elif treeNode.rule.name == '<инициализация переменной>':
#             result += self.__generateInitVar(treeNode)
#
#         return result
#
#     def __generateUpdateVar(self, treeNode):
#         if treeNode.children[0].rule.name == '<унарный алгебраический оператор>':
#             varName = treeNode.children[1].lexeme.lexeme
#             operator = treeNode.children[0].lexeme.lexeme
#             if operator == '++':
#                 result = f'Inc({varName})'
#             else:
#                 result = f'Dec({varName})'
#         else:
#             varName = treeNode.children[0].lexeme.lexeme
#             if treeNode.children[1].rule.name == '<унарный алгебраический оператор>':
#                 operator = treeNode.children[1].lexeme.lexeme
#                 if operator == '++':
#                     result = f'Inc({varName})'
#                 else:
#                     result = f'Dec({varName})'
#             else:
#                 expVal = self.__generateExpression(treeNode.children[1], 0)
#                 result = f'{varName} := {expVal}'
#
#         return result
#
#     def __generateInitVar(self, treeNode):
#         varType = treeNode.children[0].lexeme.lexeme
#         varName = treeNode.children[1].lexeme.lexeme
#         expVal = self.__generateExpression(treeNode.children[2], 0)
#         if expVal != '':
#             result = f'var {varName}: {varType} := {expVal}'
#         else:
#             result = f'var {varName}: {varType}'
#         return result
#
#     def __generateFor(self, treeNode):
#         firstExp = self.__generate_Helper(treeNode.children[0], 0)
#         secondExp = self.__generate_Helper(treeNode.children[1], 0)
#         thirdExp = self.__generate_Helper(treeNode.children[2], 0)
#         body = self.__generate_Helper(treeNode.children[3], level + 1)
#
#         return f'{INDENT * level}{firstExp};\n'\
#                f'{INDENT * level}while {secondExp} do\n'\
#                f'{body}\n' \
#                f'{INDENT * (level + 1)}{thirdExp}\n'
#
#     def __generateWhile(self, treeNode, level):
#         return
#
#     def __generateExpression(self, treeNode, level):
#         result = INDENT * level
#
#         if treeNode.rule.name == '<вызов функции>':
#             result += self.__generateFunCall(treeNode, 0)
#         elif treeNode.rule.name == '<имя переменной>' or \
#                 treeNode.rule.name == '<число>' or \
#                 treeNode.rule.name == '<бинарный алгебраический оператор>' or \
#                 treeNode.rule.name == '<булева константа>' or \
#                 treeNode.rule.name == '<оператор сравнения>':
#             result += treeNode.lexeme.lexeme
#
#         for child in treeNode.children:
#             result += self.__generateExpression(child, level)
#
#         return result
#
#     def __generate_Helper(self, treeNode):
#         if treeNode.rule.name == '<главная функция>':
#             return self.__generateMain(treeNode)
#         elif treeNode.rule.name == '<цикл for>':
#             return self.__generateFor(treeNode)
#         elif (treeNode.rule.name == '<обновление переменной>') or (treeNode.rule.name == '<инициализация переменной>'):
#             return self.__generateVar(treeNode)
#         elif treeNode.rule.name == '<выражение>' or treeNode.rule.name == '<булево выражение>':
#             return self.__generateExpression(treeNode)
#         else:
#             result = ''
#             for child in treeNode.children:
#                 result += self.__generate_Helper(child)
#             return result
#
#     def generate(self):
#         return self.__generate_Helper(self.tree)
