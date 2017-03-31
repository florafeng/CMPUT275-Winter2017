
# Parsing information goes here at top level, not in a class
# import sys
# sys.path.insert(0, "../..")

# if sys.version_info[0] >= 3:
    # raw_input = input

tokens = [ 'NAME', 'NUMBER' ] 

literals = ['=', '+', '-', '*', '/', '(', ')']

# Tokens

t_NAME = r'[a-zA-Z_][a-zA-Z0-9_]*'

def t_NUMBER(t):
    r'\d+'
    t.value = int(t.value)
    return t

t_ignore = " \t"


def t_newline(t):
    r'\n+'
    t.lexer.lineno += t.value.count("\n")


def t_error(t):
    print("Illegal character '%s'" % t.value[0])
    t.lexer.skip(1)

# Build the lexer
# import ply.lex as lex
# lex.lex()

# Parsing rules

precedence = (
    ('left', '+', '-'),
    ('left', '*', '/'),
    ('right', 'UMINUS'),
)

# Grammar rules

def p_statement_assign(p):
    'statement : NAME "=" expression'
    p[0] = [ "=", p[1] ]


def p_statement_expr(p):
    'statement : expression'
    # return the parse tree
    p[0] = p[1]


def p_expression_binop(p):
    '''expression : expression '+' expression
                  | expression '-' expression
                  | expression '*' expression
                  | expression '/' expression'''
    p[0] = [ p[2], p[1], p[3] ]

def p_expression_uminus(p):
    "expression : '-' expression %prec UMINUS"
    p[0] = [ "neg", p[2] ]


def p_expression_group(p):
    "expression : '(' expression ')'"
    p[0] = p[2]


def p_expression_number(p):
    "expression : NUMBER"
    p[0] = p[1]


def p_expression_name(p):
    "expression : NAME"
    p[0] = p[1]

def p_error(p):
    if p:
        print("Syntax error at '%s'" % p.value)
    else:
        print("Syntax error at EOF")

class ExprParser():
    """
    Expression parser class

    >>> p = ExprParser()
    >>> p.parse("1 + 2") 
    ['+', 1, 2]

    >>> p.parse("x + 2") 
    ['+', 'x', 2]

    >>> p.parse("y + 2") 
    ['+', 'y', 2]

    """

    def __init__(self):
        # Build the lexer and parser, and save them as instance variables
        import ply.lex as lex
        import ply.yacc as yacc
        self.lexer = lex.lex()
        self.parser = yacc.yacc()

    def parse(self, s):

        result = self.parser.parse(s, lexer=self.lexer)

        return result
        

if __name__ == "__main__":
    import doctest
    doctest.testmod()
