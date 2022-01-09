from Parser.Earley import *
from Parser.GrammarParser import *
from Lexer.LexicalAnalyzer import *
from pptree import *
import re

if __name__ == '__main__':
    lexicalAnalyzer = LexicalAnalyzer('test.cpp')
    lexicalAnalyzer.startParsing()
    lexicalAnalyzer.printLexemes()
    lexicalAnalyzer.printErrors()

    # grammarParser = GrammarParser()
    # grammarParser.parseJsonRules('grammar.json')
    # grammarParser.printRules()

    earley = Earley()


    # N = Rule("<выражение>", Production("13"))
    # VN = Rule("<имя переменной>", Production("a"), Production("main"))
    # DT = Rule("<тип данных>", Production("int"), Production("void"))
    # VI = Rule("<инициализация переменной>", Production(DT, VN, "=", N))
    # I = Rule("<инструкция>", Production(VI, ";"))
    # PB = Rule("<тело процедуры>", Production(I))
    # SEP = Rule("<разделитель>", Production("("), Production(")"), Production("{"), Production("}"))
    # MF = Rule("<главная функция>", Production(DT, "main", "(", ")", "{", PB, "}"))
    # SS = Rule("<программа>", Production(MF))
    #
    # G = Rule("G", Production("g"))
    # D = Rule("D", Production("dd"))
    # F = Rule("F", Production("ffff"))
    # E = Rule("E", Production("eee"))
    # C = Rule("C", Production(D, G))
    # B = Rule("B", Production(E, F))
    # A = Rule("A", Production(B, C))

    # earleyTable = earley.parse(SS, "void main ( ) { int a = 13 ; }")
    # earleyTable = earley.parse(A, "eee ffff dd g")
    # print_tree(earleyTable[0].states[0], nameattr='self')
    # treeBuilder = TreeBuilder(earleyTable)
    # tree = treeBuilder.build_tree()
    # treeBuilder.printTree(tree)
    # treeBuilder.printTree(tree)
    # table = earley.parse(SS, "void main ( ) { int a = 13 ; }")
    # print_tree(tree, nameattr='value')
    # print_tree(earleyTable[0].states[0], nameattr='self')
    print()