from purplex import Lexer, TokenDef
from purplex import Parser, attach
from purplex import LEFT, RIGHT

from type_defs import *
from term_defs import *

import ast


class MyLexer(Lexer):

    COLON = TokenDef(r':')
    # ASSIGN = TokenDef(r':=')
    ARROW = TokenDef(r'->')
    LPAREN = TokenDef(r'\(')
    RPAREN = TokenDef(r'\)')
    LBRAC = TokenDef(r'\{')
    RBRAC = TokenDef(r'\}')
    BACKSLASH = TokenDef(r'\\')
    STRAIGHT = TokenDef(r'\|')
    POINT = TokenDef(r'\.')
    COMMA = TokenDef(r'\,')

    # FUNCTION = TokenDef(r'fun')
    # SEMICOLON = TokenDef(r'\;')

    IF = TokenDef(r'if')
    THEN = TokenDef(r'then')
    ELSE = TokenDef(r'else')

    INTEGERTYPE = TokenDef(r'int')
    FLOATTYPE = TokenDef(r'float')
    STRINGTYPE = TokenDef(r'string')
    BOOLTYPE = TokenDef(r'bool')

    PLUS = TokenDef(r'\+')
    MINUS = TokenDef(r'-')
    TIMES = TokenDef(r'\*')
    DIV = TokenDef(r'/')
    LE = TokenDef(r'<=')
    GE = TokenDef(r'>=')
    EQ = TokenDef(r'==')
    LT = TokenDef(r'<')
    GT = TokenDef(r'>')

    WHITESPACE = TokenDef(r'[\s\n]+', ignore=True)
    BOOLEAN = TokenDef(r'(true | false)')
    FLOAT = TokenDef(r'\d+\.\d+')
    INTEGER = TokenDef(r'\d+')
    VARNAME = TokenDef(r'[a-zA-Z_][a-zA-Z0-9_]*')
    STRING = TokenDef(r'"[^"]*"')

class MyParser(Parser):

    LEXER = MyLexer
    START = 'e'

    PRECEDENCE = (
        (LEFT, 'TIMES', 'DIV'),
        (LEFT, 'PLUS', 'MINUS'),
    )

    # @attach('e : e SEMICOLON e')
    # def splitexp(self, left, scolon, right):
    #     return Seq(left, right)

    @attach('e : e SEMICOLON')
    def splitexpend(self, left, scolon):
        return left

    # @attach('e : VARNAME ASSIGN e')
    # def defvar(self, varname, ass, right):
    #     return Assign(Var(varname), right)
    
    # @attach('e : FUN LPAREN e COLON e RPAREN LBRAC e RBRAC ')
    # def fundef(self, fun, lp, arg, col, gtype, rp, lb, body, rb):
    #     return Abs(arg, gtype, body)

    @attach('e : BACKSLASH e COLON e POINT e ')
    def fundef(self, bs, arg, col, gtype, pt, body):
        return Abs(arg, gtype, body)

    @attach('e : INTEGER')
    def const_int(self, integer):
        return Integer(int(integer))

    @attach('e : FLOAT')
    def const_float(self, _float):
        return Float(float(_float))

    @attach('e : BOOLEAN')
    def const_bool(self, _bool):
        return Boolean(str(_bool))

    @attach('e : LBRAC e RBRAC')
    def record(self, lbrac, content, rbrac):
        if content[1] == "val":
            return Record(content[0])
        return RType(content[0])

    @attach('e : LPAREN e RPAREN')
    def parens(self, lp, body, rp):
        return body

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

    @attach('e : e ARROW e')
    def compositefunctiontype(self, lefttype, arrow, righttype):
        return CType(lefttype, righttype)
    
    @attach('e : VARNAME')
    def var(self, string):
        return Var(string)

    @attach('e : STRING EQ e COMMA e')
    def record_list_head(self, label, eq, val, comma, tail):
        d = dict()
        d[label] = val
        return (d.update(tail[0]), "val")
    
    @attach('e : STRING EQ e')
    def record_list_tail(self, label, eq, val):
        d = dict()
        d[label] = val
        return (d, "val")

    @attach('e : STRING COLON e COMMA e')
    def record_type_list_head(self, label, eq, val, comma, tail):
        d = dict()
        d[label] = val
        return (d.update(tail[0]), "type")
    
    @attach('e : STRING COLON e')
    def record_type_list_tail(self, label, eq, val):
        d = dict()
        d[label] = val
        return (d, "type")
    
    @attach('e : STRING')
    def const_str(self, string):
        return String(str(string))
    
    # @attach('e : e e')
    # def application(self, left, right):
    #     return App(left, right)
