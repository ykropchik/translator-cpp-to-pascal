from source.Lexer.LexicalAnalyzer import LexicalAnalyzer
from Parser.Earley import *
import re

if __name__ == '__main__':
    # grammarParser = GrammarParser('grammar.txt')
    # grammarParser.parseRules()
    # lexicalAnalyzer = LexicalAnalyzer('test.cpp')
    #
    # lexicalAnalyzer.startParsing()
    # lexicalAnalyzer.printLexemes()
    # lexicalAnalyzer.printErrors()
    C = Rule("C", Production("c"))
    B = Rule("B", Production("b"), Production("g"))
    A = Rule("A", Production(B))
    S = Rule("S", Production(A, B, C))

    earley = Earley()
    earley.parse(S, "b g c")