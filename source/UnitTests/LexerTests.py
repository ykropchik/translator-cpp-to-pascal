import unittest
from source.Lexer.LexicalAnalyzer import LexicalAnalyzer


class LexerTests(unittest.TestCase):
    def setUp(self):
        self.lexicalAnalyzer = LexicalAnalyzer('lexerUnitTestFile.cpp')
        self.lexicalAnalyzer.startParsing()

    def test_LexemeType_Plus(self):
        self.assertEqual(self.lexicalAnalyzer.returnLexemes(0), 'PLUS')

    def test_LexemeType_Increment(self):
        self.assertEqual(self.lexicalAnalyzer.returnLexemes(1), 'INCREMENT')

    def test_LexemeType_Minus(self):
        self.assertEqual(self.lexicalAnalyzer.returnLexemes(2), 'MINUS')

    def test_LexemeType_Decrement(self):
        self.assertEqual(self.lexicalAnalyzer.returnLexemes(3), 'DECREMENT')

    def test_LexemeType_Multiplication(self):
        self.assertEqual(self.lexicalAnalyzer.returnLexemes(4), 'MULTIPLICATION')

    def test_LexemeType_Division(self):
        self.assertEqual(self.lexicalAnalyzer.returnLexemes(5), 'DIVISION')

    def test_LexemeType_Mod(self):
        self.assertEqual(self.lexicalAnalyzer.returnLexemes(6), 'MOD')

    def test_LexemeType_Assignment(self):
        self.assertEqual(self.lexicalAnalyzer.returnLexemes(7), 'ASSIGNMENT')

    def test_LexemeType_Equal(self):
        self.assertEqual(self.lexicalAnalyzer.returnLexemes(8), 'EQUAL')

    def test_LexemeType_NotEqual(self):
        self.assertEqual(self.lexicalAnalyzer.returnLexemes(9), 'NOT_EQUAL')

    def test_LexemeType_LessThan(self):
        self.assertEqual(self.lexicalAnalyzer.returnLexemes(10), 'LESS_THAN')

    def test_LexemeType_MoreThan(self):
        self.assertEqual(self.lexicalAnalyzer.returnLexemes(11), 'MORE_THAN')

    def test_LexemeType_LessOrEqual(self):
        self.assertEqual(self.lexicalAnalyzer.returnLexemes(12), 'LESS_OR_EQUAL')

    def test_LexemeType_MoreOrEqual(self):
        self.assertEqual(self.lexicalAnalyzer.returnLexemes(13), 'MORE_OR_EQUAL')

    def test_LexemeType_Not(self):
        self.assertEqual(self.lexicalAnalyzer.returnLexemes(14), 'NOT')

    def test_LexemeType_And(self):
        self.assertEqual(self.lexicalAnalyzer.returnLexemes(15), 'AND')

    def test_LexemeType_Or(self):
        self.assertEqual(self.lexicalAnalyzer.returnLexemes(16), 'OR')

    def test_LexemeType_Void(self):
        self.assertEqual(self.lexicalAnalyzer.returnLexemes(17), 'VOID')

    def test_LexemeType_Int(self):
        self.assertEqual(self.lexicalAnalyzer.returnLexemes(18), 'INT')

    def test_LexemeType_Long(self):
        self.assertEqual(self.lexicalAnalyzer.returnLexemes(19), 'LONG')

    def test_LexemeType_Short(self):
        self.assertEqual(self.lexicalAnalyzer.returnLexemes(20), 'SHORT')

    def test_LexemeType_Unsigned(self):
        self.assertEqual(self.lexicalAnalyzer.returnLexemes(21), 'UNSIGNED')

    def test_LexemeType_Bool(self):
        self.assertEqual(self.lexicalAnalyzer.returnLexemes(22), 'BOOL')

    def test_LexemeType_Float(self):
        self.assertEqual(self.lexicalAnalyzer.returnLexemes(23), 'FLOAT')

    def test_LexemeType_Double(self):
        self.assertEqual(self.lexicalAnalyzer.returnLexemes(24), 'DOUBLE')

    def test_LexemeType_Char(self):
        self.assertEqual(self.lexicalAnalyzer.returnLexemes(25), 'CHAR')

    def test_LexemeType_For(self):
        self.assertEqual(self.lexicalAnalyzer.returnLexemes(26), 'FOR')

    def test_LexemeType_While(self):
        self.assertEqual(self.lexicalAnalyzer.returnLexemes(27), 'WHILE')

    def test_LexemeType_If(self):
        self.assertEqual(self.lexicalAnalyzer.returnLexemes(28), 'IF')

    def test_LexemeType_Else(self):
        self.assertEqual(self.lexicalAnalyzer.returnLexemes(29), 'ELSE')

    def test_LexemeType_True(self):
        self.assertEqual(self.lexicalAnalyzer.returnLexemes(30), 'TRUE')

    def test_LexemeType_False(self):
        self.assertEqual(self.lexicalAnalyzer.returnLexemes(31), 'FALSE')

    def test_LexemeType_Include(self):
        self.assertEqual(self.lexicalAnalyzer.returnLexemes(32), 'INCLUDE')

    def test_LexemeType_Std(self):
        self.assertEqual(self.lexicalAnalyzer.returnLexemes(33), 'STD')

    def test_LexemeType_Main(self):
        self.assertEqual(self.lexicalAnalyzer.returnLexemes(34), 'MAIN')

    def test_LexemeType_Return(self):
        self.assertEqual(self.lexicalAnalyzer.returnLexemes(35), 'RETURN')

    def test_LexemeType_Cout(self):
        self.assertEqual(self.lexicalAnalyzer.returnLexemes(36), 'COUT')

    def test_LexemeType_Cin(self):
        self.assertEqual(self.lexicalAnalyzer.returnLexemes(37), 'CIN')

    def test_LexemeType_Abs(self):
        self.assertEqual(self.lexicalAnalyzer.returnLexemes(38), 'ABS')

    def test_LexemeType_Sqr(self):
        self.assertEqual(self.lexicalAnalyzer.returnLexemes(39), 'SQR')

    def test_LexemeType_Sqrt(self):
        self.assertEqual(self.lexicalAnalyzer.returnLexemes(40), 'SQRT')

    def test_LexemeType_Pow(self):
        self.assertEqual(self.lexicalAnalyzer.returnLexemes(41), 'POW')

    def test_LexemeType_Floor(self):
        self.assertEqual(self.lexicalAnalyzer.returnLexemes(42), 'FLOOR')

    def test_LexemeType_Ceil(self):
        self.assertEqual(self.lexicalAnalyzer.returnLexemes(43), 'CEIL')

    def test_LexemeType_RoundOpenBracket(self):
        self.assertEqual(self.lexicalAnalyzer.returnLexemes(44), 'ROUND_OPEN_BRACKET')

    def test_LexemeType_RoundCloseBracket(self):
        self.assertEqual(self.lexicalAnalyzer.returnLexemes(45), 'ROUND_CLOSE_BRACKET')

    def test_LexemeType_CurlyOpenBracket(self):
        self.assertEqual(self.lexicalAnalyzer.returnLexemes(46), 'CURLY_OPEN_BRACKET')

    def test_LexemeType_CurlyCloseBracket(self):
        self.assertEqual(self.lexicalAnalyzer.returnLexemes(47), 'CURLY_CLOSE_BRACKET')

    def test_LexemeType_SquareOpenBracket(self):
        self.assertEqual(self.lexicalAnalyzer.returnLexemes(48), 'SQUARE_OPEN_BRACKET')

    def test_LexemeType_SquareCloseBracket(self):
        self.assertEqual(self.lexicalAnalyzer.returnLexemes(49), 'SQUARE_CLOSE_BRACKET')

    def test_LexemeType_SemiColon(self):
        self.assertEqual(self.lexicalAnalyzer.returnLexemes(50), 'SEMICOLON')

    def test_LexemeType_Colon(self):
        self.assertEqual(self.lexicalAnalyzer.returnLexemes(51), 'COLON')


if __name__ == '__main__':
    unittest.main()
