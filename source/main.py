from source.Lexer.LexicalAnalyzer import LexicalAnalyzer
import re

if __name__ == '__main__':
    lexicalAnalyzer = LexicalAnalyzer('test.cpp')

    lexicalAnalyzer.startParsing()
    lexicalAnalyzer.printLexemes()
    lexicalAnalyzer.printErrors()
