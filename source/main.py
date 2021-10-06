from source.Lexer.LexicalAnalyzer import LexicalAnalyzer

if __name__ == '__main__':
    with open('test.cpp', 'r') as file:
        lexicalAnalyzer = LexicalAnalyzer(file.read())

    lexicalAnalyzer.startParsing()
    lexicalAnalyzer.printLexemes()
