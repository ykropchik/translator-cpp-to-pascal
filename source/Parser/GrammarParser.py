import re

from source.Parser.Earley import Rule


class GrammarParser:
    def __init__(self, filePath):
        self.file = open(filePath, 'r', encoding="utf-8")
        self.errorLineNumbers = []

    def parseRules(self):
        result = []
        lineNumber = 0
        for line in self.file.readlines():
            lineNumber += 1
            if bool(re.search('^<.+>->.+$', line)):
                marchingResult = re.search('^(<.+>)->', line)
                rightSide = line.replace('\n', '').split('->')[1].split('|')
                newRule = Rule(marchingResult.group(1), rightSide)
                result.append(newRule)
            else:
                self.errorLineNumbers.append(lineNumber)
        for rule in result:
            rule.print()

        print()

        print('Parsing finished with ', len(self.errorLineNumbers), ' errors')
        for number in self.errorLineNumbers:
            print('Error in line ', number)