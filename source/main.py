from source.Lexer.LexicalAnalyzer import *
from source.Parser.GrammarParser import *
from source.CodeGenerator.Generator import *
from source.Semantic_Analyzer.SemanticAnalyzer import *
from source.Optimizer.Optimizer import *

if __name__ == '__main__':
    print("-" * 10, "Lexer", "-" * 10)

    lexicalAnalyzer = LexicalAnalyzer('test.cpp')
    lexicalAnalyzerResult = lexicalAnalyzer.startParsing()
    # lexicalAnalyzer.printLexemes()
    lexicalAnalyzer.printErrors()

    print()
    if lexicalAnalyzerResult:
        print("-"*10, "Grammar", "-"*10)

        grammarParser = GrammarParser()
        grammarParser.parseJsonRules('grammar.json')
        # grammarParser.printRules()

        earley = Earley(grammarParser.rules, "<программа>")

        earleyParseResult = earley.parse(lexicalAnalyzer.lexemeArray)
        earley.printTableToFile()
        earley.printError()
        earleyTable = earley.table

        # exit(-1)

        if earleyParseResult:
            treeBuilder = TreeBuilder(earleyTable, grammarParser.rules)

            # treeBuilder.build_tree()
            treeBuilder.buildTree()
            treeBuilder.printTreeToFile()

            # generator = Generator(treeBuilder.tree)
            # generator.generate()
            # print(generator.resultCode)

            # variableStorage = VariableStorage()
            #
            # print('_________________')
            # semanticAnalyser = VariableSemanticAnalyser(treeBuilder.tree)
            # semanticAnalyser.parse(treeBuilder.tree, variableStorage)

            optimizer = Optimizer(treeBuilder.tree)
            optimizer.optimize()

    print()