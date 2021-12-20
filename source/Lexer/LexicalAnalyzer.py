from source.Lexer.LexemeType import LexemeType
from source.Lexer.LexemeType import DictionaryOfLexemes
import re


class LexicalAnalyzer:
    class LexemeArrayType:
        def __init__(self, lexeme, lexemeType, lineNumber):
            self.lexeme = lexeme
            self.lexemeType = lexemeType
            self.lineNumber = lineNumber

    class ErrorType:
        def __init__(self, lineNumber, word):
            self.lineNumber = lineNumber
            self.word = word

    def __init__(self, fileName):
        self.inputFile = open(fileName, 'r')
        self.lexemeArray = []
        self.errors = []

    def __del__(self):
        self.inputFile.close()

    def __removeSpaces(self, line):
        # self.inputFile = self.inputFile.replace("\n", "")
        return " ".join(line.split())

    def __splitBySeparators(self, line):
        resultLine = " ( ".join(line.split("("))
        resultLine = " ) ".join(resultLine.split(")"))
        resultLine = " [ ".join(resultLine.split("["))
        resultLine = " ] ".join(resultLine.split("]"))
        resultLine = " { ".join(resultLine.split("{"))
        resultLine = " } ".join(resultLine.split("}"))
        resultLine = " ; ".join(resultLine.split(";"))
        return " : ".join(resultLine.split(":")).rstrip()

    def __checkBySymbol(self, word, lineNumber):
        if re.match('^-?\d+\.?$', word):
            self.lexemeArray.append(self.LexemeArrayType(word, LexemeType.INT_NUMBER, lineNumber))
            return

        if re.match('^-?\d+.?\d+[e|E]{1}[+|-]?\d+$', word):
            self.lexemeArray.append(self.LexemeArrayType(word, LexemeType.EXPONENTIAL_NUMBER, lineNumber))
            return

        if re.match('^-?\d*.\d+$', word):
            self.lexemeArray.append(self.LexemeArrayType(word, LexemeType.REAL_NUMBER, lineNumber))
            return

        if re.match('^\+\+$', word):
            self.lexemeArray.append(self.LexemeArrayType(word, LexemeType.INCREMENT, lineNumber))
            return

        if re.match('^--$', word):
            self.lexemeArray.append(self.LexemeArrayType(word, LexemeType.DECREMENT, lineNumber))
            return

        if re.match('^\+\+.+', word):
            self.lexemeArray.append(self.LexemeArrayType('++', LexemeType.INCREMENT, lineNumber))
            self.__checkBySymbol(word.removeprefix('++'), lineNumber)
            return

        if re.match('.+\+\+$', word):
            self.__checkBySymbol(word.removesuffix('++'), lineNumber)
            self.lexemeArray.append(self.LexemeArrayType('++', LexemeType.INCREMENT, lineNumber))
            return

        if re.match('^--.+', word):
            self.lexemeArray.append(self.LexemeArrayType('--', LexemeType.DECREMENT, lineNumber))
            self.__checkBySymbol(word.removeprefix('--'), lineNumber)
            return

        if re.match('.+--$', word):
            self.__checkBySymbol(word.removesuffix('--'), lineNumber)
            self.lexemeArray.append(self.LexemeArrayType('--', LexemeType.DECREMENT, lineNumber))
            return

        if re.match('^[A-z_-]+[A-z_-|\d]*$', word):
            self.lexemeArray.append(self.LexemeArrayType(word, LexemeType.NAME, lineNumber))
            return

        self.errors.append(self.ErrorType(lineNumber, word))
        self.lexemeArray.append(self.LexemeArrayType(word, LexemeType.UNDEFINED, lineNumber))

    def startParsing(self):
        lineNumber = 0
        for line in self.inputFile.readlines():
            lineNumber += 1
            splitedLine = self.__splitBySeparators(line)
            if splitedLine != '':
                for word in splitedLine.split():
                    try:
                        self.lexemeArray.append(self.LexemeArrayType(word, DictionaryOfLexemes[word], lineNumber))
                    except KeyError as e:
                        self.__checkBySymbol(word, lineNumber)

    def printErrors(self):
        for error in self.errors:
            print("Line: %s - Word: %s" % (error.lineNumber, error.word))

    def printLexemes(self):
        width = max(map(lambda lexeme: len(lexeme.lexemeType.name), self.lexemeArray)) + 1
        for lexeme in self.lexemeArray:
            print("Line: %s - [ %s ] - %s" % (lexeme.lineNumber, lexeme.lexemeType.name.rjust(width), lexeme.lexeme))

    def returnLexemes(self, testCaseNumber):
        return self.lexemeArray[testCaseNumber].lexemeType.name