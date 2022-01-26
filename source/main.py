from source.Lexer.LexicalAnalyzer import *
from source.Parser.GrammarParser import *
from source.Semantic_Analyzer.SemanticAnalyzer import VariableSemanticAnalyser
from pptree import *

if __name__ == '__main__':
    print("-" * 10, "Lexer", "-" * 10)

    lexicalAnalyzer = LexicalAnalyzer('test.cpp')
    lexicalAnalyzer.startParsing()
    lexicalAnalyzer.printLexemes()
    # lexicalAnalyzer.printErrors()

    print()
    print("-"*10, "Grammar", "-"*10)

    grammarParser = GrammarParser()
    grammarParser.parseJsonRules('grammar.json')
    # grammarParser.printRules()

    earley = Earley(grammarParser.rules, "<программа>")

    def convertArray(array):
        temp = (LexemeType.WORD, LexemeType.INT_NUMBER, LexemeType.REAL_NUMBER, LexemeType.EXPONENTIAL_NUMBER)
        result = []
        for item in array:
            result.extend(list(item.lexeme)) if item.lexemeType in temp else result.append(item.lexeme)
        return result

    parseResult = earley.parse(lexicalAnalyzer.lexemeArray)
    earley.printTable()
    earleyTable = earley.table

    if parseResult:
        treeBuilder = TreeBuilder(earleyTable)
        # for st in earleyTable[-1]:
        #     if st.name == GAMMA_RULE and st.completed():
        #         gammaRule = st
        #
        # testTree = treeBuilder.build_tree_test(gammaRule)
        # treeBuilder.printTreeToFileTest(testTree)

        treeBuilder.build_tree()
        treeBuilder.printTreeToFile()

        print('_________________')
        semanticAnalyser = VariableSemanticAnalyser(treeBuilder.tree)
        semanticAnalyser.parse(treeBuilder.tree)
    # treeBuilder.printTree()

    # N = Rule("<выражение>", Production("13"))
    # VN = Rule("<имя переменной>", Production("a"), Production("main"))
    # DT = Rule("<тип данных>", Production("int"), Production("void"))
    # VI = Rule("<инициализация переменной>", Production(DT, VN, "=", N))
    # I = Rule("<инструкция>", Production(VI, ";"))
    # PB = Rule("<тело процедуры>", Production(I))
    # SEP = Rule("<разделитель>", Production("("), Production(")"), Production("{"), Production("}"))
    # MF = Rule("<главная функция>", Production(DT, "main", "(", ")", "{", PB, "}"))
    # SS = Rule("<программа>", Production(MF))
    # rules = [N, VN, DT, VI, I, PB, SEP, MF, SS]
    #
    # G = Rule("G", Production("g"))
    # D = Rule("D", Production("dd"))
    # F = Rule("F", Production("ffff"))
    # E = Rule("E", Production("eee"))
    # C = Rule("C", Production(D, G))
    # B = Rule("B", Production(E, F))
    # A = Rule("A", Production(B, C))

    # earley = Earley(rules, "<программа>")
    # earleyTable = earley.parse(["void", "main", "(", ")", "{", "int", "a", "=", "13", ";", "}"])
    # earleyTable = earley.parse(A, "eee ffff dd g")
    # print_tree(earleyTable[0].states[0], nameattr='self')
    # treeBuilder = TreeBuilder(earleyTable)
    # tree = treeBuilder.build_tree()
    # treeBuilder.printTree()
    # treeBuilder.printTree(tree)
    # table = earley.parse(SS, "void main ( ) { int a = 13 ; }")
    # print_tree(tree, nameattr='value')
    # print_tree(earleyTable[0].states[0], nameattr='self')
    print()