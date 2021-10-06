from source.Lexer.LexemeType import LexemeType
from source.Lexer.LexemeType import DictionaryOfLexemes


class LexicalAnalyzer:
    class LexemeArrayType:
        def __init__(self, lexeme, lexemeType):
            self.lexeme = lexeme
            self.lexemeType = lexemeType

    class ErrorType:
        def __init__(self, errorType, lineNumber):
            self.errorType = errorType
            self.lineNumber = lineNumber

    def __init__(self, inputText):
        self.inputText = inputText
        self.pointer = 0
        self.lexemeArray = []
        self.errors = []

    def __getLexeme(self):
        return 1

    def __removeSpaces(self):
        self.inputText = self.inputText.replace("\n", "")
        self.inputText = " ".join(self.inputText.split())
        return 1

    def __splitBySeparators(self):
        self.inputText = " ( ".join(self.inputText.split("("))
        self.inputText = " ) ".join(self.inputText.split(")"))
        self.inputText = " [ ".join(self.inputText.split("["))
        self.inputText = " ] ".join(self.inputText.split("]"))
        self.inputText = " { ".join(self.inputText.split("{"))
        self.inputText = " } ".join(self.inputText.split("}"))
        self.inputText = " ; ".join(self.inputText.split(";"))
        self.inputText = " : ".join(self.inputText.split(":"))

    def __checkBySymbol(self, word):
        # if (word[0].isDigit):
        #     for char in word:

        return LexemeType.UNDEFINED

    def startParsing(self):
        self.__removeSpaces()
        self.__splitBySeparators()

        for word in self.inputText.split():
            try:
                self.lexemeArray.append(self.LexemeArrayType(word, DictionaryOfLexemes[word]))
            except KeyError as e:
                self.lexemeArray.append(self.LexemeArrayType(word, self.__checkBySymbol(word)))

        return 1

    def printLexemes(self):
        width = max(map(lambda lexeme: len(lexeme.lexemeType.name), self.lexemeArray)) + 1
        for lexeme in self.lexemeArray:
            print("%s - " % lexeme.lexemeType.name.rjust(width), lexeme.lexeme, sep='')
            # print(, ' - ', lexeme.lexemeType)
