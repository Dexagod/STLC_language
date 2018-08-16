from purplex import Lexer, TokenDef
from purplex import Parser, attach
from purplex import LEFT, RIGHT

from type_defs import *
from term_defs import *

from ast import literal_eval

class MyLexer(Lexer):

    COLON = TokenDef(r':')
    DARROW = TokenDef(r'=>')

    LPAREN = TokenDef(r'\(')
    RPAREN = TokenDef(r'\)')
    LBRACE = TokenDef(r'\{')
    RBRACE = TokenDef(r'\}')
    LBRACKET = TokenDef(r'\[')
    RBRACKET = TokenDef(r'\]')
    LHOOK = TokenDef(r'\<\<')
    RHOOK = TokenDef(r'\>\>')
    BACKSLASH = TokenDef(r'\\')
    SEMICOL = TokenDef(r'\;')
    POINT = TokenDef(r'\.')
    COMMA = TokenDef(r',')
    STRAIGHT = TokenDef(r'\|')

    OP = TokenDef(r'(\<-|-\>|\+|-|\*|\/|\<=|\>=|==|\<|\>)')

    ASSIGN = TokenDef(r'=')
    
    IF = TokenDef(r'if')
    THEN = TokenDef(r'then')
    ELSE = TokenDef(r'else')
    FI = TokenDef(r'fi')
    END = TokenDef(r'end')
    
    CASE = TokenDef(r'case')
    OF = TokenDef(r'of')
    AS = TokenDef(r'as')
    SA = TokenDef(r'sa')
    FIX = TokenDef(r'fix')

    START = TokenDef(r'start')
    STOP = TokenDef(r'stop')

    INTEGERTYPE = TokenDef(r'int')
    FLOATTYPE = TokenDef(r'float')
    STRINGTYPE = TokenDef(r'string')
    BOOLTYPE = TokenDef(r'bool')
    


    WHITESPACE = TokenDef(r'[\s\n]+', ignore=True)

    BOOLEAN = TokenDef(r'(true|True|False|false)')
    FLOAT = TokenDef(r'\d+\.\d+')
    INTEGER = TokenDef(r'\d+')
    VARNAME = TokenDef(r'[a-zA-Z_][a-zA-Z0-9_]*')
    STRING = TokenDef(r'"[^"]*"')


class MyParser(Parser):

    LEXER = MyLexer
    START = 'e'

    @attach('e : START e STOP COMMA e')
    def arrayfi(self, start, exp, stop, comma, tail):
        return  [exp] + tail
    

    @attach('e : START e STOP')
    def arrayfiend(self, start, exp, stop):
        return  [exp]

    @attach('e : LPAREN e RPAREN')
    def brackets(self, lparen, expr, rparen):
        return  expr 
    
    @attach('e : BACKSLASH VARNAME COLON e POINT e END')
    def lambda_abstraction(self, lambda_token, param, colon, giventype, point, body, abstr_end):
        return Abs(Var(param), giventype, body)

    @attach('e : IF e THEN e ELSE e FI')
    def if_stmt(self, i, cond, t, a, e, b, fi):
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
        if "false" in _bool or "False" in _bool:
            return(Boolean(False))
        return Boolean(True)

    @attach('e : LBRACE VARNAME ASSIGN e COMMA e')
    def recordhead(self, lbrace, left, assign, right, delim, tail):
        d = dict()
        d[str(left)] = right
        d.update(dict(tail))
        return Record(d)
    
    @attach('e : VARNAME ASSIGN e COMMA e')
    def recordmid(self, left, assign, right, delim, tail):
        d = dict()
        d[str(left)] = right
        d.update(dict(tail))
        return d

    @attach('e : VARNAME ASSIGN e RBRACE')
    def recordtail(self, left, assign, right, rbrace):
        d = dict()
        d[str(left)] = right
        return d  

    @attach('e : LBRACE VARNAME COLON e COMMA e')
    def recordtypehead(self, lbrace, left, assign, right, delim, tail):
        d = dict()
        d[str(left)] = right
        d.update(dict(tail))
        return RType(d)

    @attach('e : VARNAME COLON e COMMA e')
    def recordtypemidandVTYPEmid(self, left, assign, right, delim, tail):
        d = dict()
        d[str(left)] = right
        d.update(dict(tail))
        return d

    @attach('e : VARNAME COLON e RBRACE')
    def recordtypetail(self, left, assign, right, rbrace):
        d = dict()
        d[str(left)] = right
        return d   
    
    @attach('e : RBRACE')
    def recordandrecordtypesignletail(self, rbrace):
        d = dict()
        return d   
    
    @attach('e : e LBRACKET VARNAME RBRACKET')
    def recordproj(self, record, brac, label, rbrac):
        return Proj(record, label)    

    @attach('e : LHOOK VARNAME ASSIGN e RHOOK AS e SA')
    def tag(self, lhook, label, assign, record, rhook, _as, varianttype, scol):
        return Tag(label, record, varianttype)  


    @attach('e : LHOOK VARNAME COLON e COMMA e')
    def vtypehead(self, lhook, label, colon, record, comma, tail):
        d = dict()
        d[str(label)] = record
        d.update(dict(tail))
        return VType(d)  

    @attach('e : VARNAME COLON e RHOOK')
    def vtypetail(self, label, colon, record, RHOOK):
        d = dict()
        d[str(label)] = record
        return d

    @attach('e : RHOOK')
    def vtypesingletail(self, label, colon, record, RHOOK):
        d = dict()
        return d   

    @attach('e : CASE e OF LBRACE VARNAME ASSIGN VARNAME DARROW e STRAIGHT e')
    def case(self, case, tag, of, lbrac, label, assign, varname, darrow, mapped_action, straight, tail):
        if type(tail) is set:
            tail.add( Map(label, Var(varname), mapped_action) )
            return Case(tag, tail)
        else:
            s = set()
            s.add( Map(label, Var(varname), mapped_action) )
            return Case(tag, s)

    @attach('e : VARNAME ASSIGN VARNAME DARROW e STRAIGHT e')
    def mapmid(self, label, ass, varname, darr, mapped_action, straight, tail):
        if type(tail) is set:
            tail.add( Map(label, Var(varname), mapped_action) )
        else:
            s = set()
            s.add( Map(label, Var(varname), mapped_action) )
            return s

    @attach('e : VARNAME ASSIGN VARNAME DARROW e RBRACE' )
    def mapend(self, label, assign, varname, darrow, mapped_action, rbrace):
        s = set()
        s.add( Map(label, Var(varname), mapped_action) )
        return s

    @attach('e : FIX e' )
    def fix(self, fix, term):
        return Fix(term)
    
    @attach('e : e OP e')
    def condit(self, left, op, right):
        if op == '<-':
            return App(left, right)
        if op == '->':
            return CType(left, right)
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


    @attach('e : STRING')
    def const_str(self, string):
        return String(str(string))

    @attach('e : VARNAME')
    def exp_var(self, string):
        return Var(str(string))