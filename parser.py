from purplex import Lexer, TokenDef
from purplex import Parser, attach
from purplex import LEFT, RIGHT

from type_defs import *
from term_defs import *

from ast import literal_eval

class MyLexer(Lexer):

    COLON = TokenDef(r':')
    ARROW = TokenDef(r'->')

    LPAREN = TokenDef(r'\(')
    RPAREN = TokenDef(r'\)')
    LBRAC = TokenDef(r'\{')
    RBRAC = TokenDef(r'\}')
    BACKSLASH = TokenDef(r'\\')
    STRAIGHT = TokenDef(r'\|')
    POINT = TokenDef(r'\.')
    COMMA = TokenDef(r',')

    OP = TokenDef(r'(\+|-|\*|\/|<=|>=|==|<|>)')

    ASSIGN = TokenDef(r'=')
    
    IF = TokenDef(r'if')
    THEN = TokenDef(r'then')
    ELSE = TokenDef(r'else')

    INTEGERTYPE = TokenDef(r'int')
    FLOATTYPE = TokenDef(r'float')
    STRINGTYPE = TokenDef(r'string')
    BOOLTYPE = TokenDef(r'bool')
    


    WHITESPACE = TokenDef(r'[\s\n]+', ignore=True)

    BOOLEAN = TokenDef(r'(true | false)')
    FLOAT = TokenDef(r'\d+\.\d+')
    INTEGER = TokenDef(r'\d+')
    VARNAME = TokenDef(r'[a-zA-Z_][a-zA-Z0-9_]*')
    STRING = TokenDef(r'"[^"]*"')


class MyParser(Parser):

    LEXER = MyLexer
    START = 'e'

    @attach('e : LPAREN e RPAREN')
    def brackets(self, lparen, expr, rparen):
        return  expr 
    
    @attach('e : BACKSLASH VARNAME COLON e POINT e STRAIGHT')
    def lambda_abstraction(self, lambda_token, param, colon, giventype, point, body, abstr_end):
        return Abs(Var(param), giventype, body)

    @attach('e : IF e THEN e ELSE e')
    def if_stmt(self, i, cond, t, a, e, b):
        return If(cond, a, b)

    @attach('e : INTEGERTYPE')
    def type_int(self, _type):
        return IntType()

    @attach('e : FLOATTYPE')
    def type_float(self, _type):
        return FloatType()

    @attach('e : STRINGTYPE')
    def type_str(self, _type):
        return StringType()

    @attach('e : BOOLTYPE')
    def type_bool(self, _type):
        return BoolType()

    @attach('e : INTEGER')
    def const_int(self, integer):
        return Integer(int(integer))

    @attach('e : FLOAT')
    def const_float(self, _float):
        return Float(float(_float))

    @attach('e : BOOLEAN')
    def const_bool(self, _bool):
        print("HERE")
        print(_bool)
        if "false" in _bool or "False" in _bool or "fls" in _bool:
            return(Boolean(False))
        return Boolean(True)

    @attach('e : STRING')
    def const_str(self, string):
        return String(str(string))

    @attach('e : VARNAME')
    def exp_var(self, string):
        return Var(str(string))
    
    @attach('e : LPAREN e ARROW e RPAREN')
    def compositefunctiontype(self, lparen, lefttype, arrow, righttype, rightparen):
        return CType(lefttype, righttype)
    

    # @attach('e : LBRAC e RBRAC')
    # def record(self, lbrac, record, rbrac):
    #     if record[1] == "value":
    #         return Record(record[0])
    #     return RType(record[0])
    


    # @attach('e : e ASSIGN e COMMA e')
    # def recordhead(self, left, assign, right, delim, tail):
    #     d = dict()
    #     d[left] = right
    #     return (d.update(tail[0]), "value")

    # @attach('e : e ASSIGN e')
    # def recordtail(self, left, assign, right):
    #     d = dict()
    #     d[left] = right
    #     return (d, "value")
    
    

    # # @attach('e : LPAREN e ARROW e RPAREN')
    # # def projection(self, lparen, lefttype, arrow, righttype, rightparen):
    # #     return CType(lefttype, righttype)

    @attach('e : e OP e')
    def condit(self, left, op, right):
        if op == '<=':
            return LE(left, right)
        if op == '>=':
            return GE(left, right)
        if op == '==':
            return EQ(left, right)
        if op == '<':
            return LT(left, right)
        if op == '>':
            return GT(left, right)
        if op == "+":
            return Plus(left, right)
        if op == "-":
            return Minus(left, right)
        if op == "*":
            return Times(left, right)
        if op == "/":
            return Div(left, right)
    
    @attach('e : e e')
    def application(self, left, right):
        return App(left, right)
