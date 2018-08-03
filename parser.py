from purplex import Lexer, TokenDef
from purplex import Parser, attach
from purplex import LEFT, RIGHT


class MyLexer(Lexer):

    INTEGER = TokenDef(r'\d+')
    STRING = TokenDef(r'&"[^\"]*"&')
    INTEGER = TokenDef(r'&[0-9]+&')
    COMMENT = TokenDef(r';.*$')
    COLON = TokenDef(r':')
    ARROW = TokenDef(r'->')
    TYPE = TokenDef(r'\$[a-zA-Z_]+')
    VARNAME = TokenDef(r'[a-zA-Z_][a-zA-Z0-9_]*')
    LPAREN = TokenDef(r'\(')
    RPAREN = TokenDef(r'\)')
    BACKSLASH = TokenDef(r'\\')
    FORWSLASH = TokenDef(r'/')
    POINT = TokenDef(r'\.')
    WHITESPACE = TokenDef(r'[\s\n]+', ignore=True)

class MyParser(Parser):

    LEXER = MyLexer
    START = 'e'

    @attach('e : e COMMENT')
    def endsemicolon(self, left, comm):
        print("Comment:", comm[1:])
        return left

    @attach('e : LPAREN e RPAREN')
    def brackets(self, lparen, expr, rparen):
        return " ( " + expr + " ) "
    
    @attach('e : BACKSLASH VARNAME COLON e POINT e FORWSLASH')
    def lambda_abstraction(self, lambda_token, param, colon, giventype, point, body, abstr_end):
        return "Abs(argument=" + param +", given_type=" + giventype + ", body=" + body + ")"

    @attach('e : INTEGER')
    def const_int(self, integer):
        return "Const( label="+ str(integer)[1:-1] + ", T='Integer')"

    @attach('e : STRING')
    def const_str(self, string):
        return "Const( label="+ str(string)[1:-1] + ", T='String')"

    @attach('e : TYPE')
    def functiontype(self, type):
        return "SType("+ str(type) + ")"

    @attach('e : LPAREN e ARROW e RPAREN')
    def compositefunctiontype(self, lparen, lefttype, arrow, righttype, rightparen):
        return "CType("+ str(lefttype) + ", " + str(righttype) + ")"
    
    @attach('e : VARNAME e')
    def simplevar(self, varname, rest):
        if rest == None:
            return "SimpleVar(label=" + str(varname) + ") " 
        else:
            return "SimpleVar(label=" + str(varname) + ") " + rest

    @attach('e : VARNAME')
    def var(self, string):
        return "Var(" + string + ")"
    
    @attach('e : e e')
    def application(self, left, right):
        return "App("+ str(left) + ", " + str(right) + ")"

if __name__ == '__main__':
    parser = MyParser()
    problems = [
        ("TEST"),
        ('\\n:(($int->$int)->($int->$int)).\\s:($int->$int).\\z:$int. s ( n s z ) /// &1& &2&'),
    ]
    for problem in problems:
        result = parser.parse(problem)
        print(result)