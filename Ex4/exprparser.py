"""
Parser for a simple caluclation expression language.
"""

from valuetree import ValueTree

# Parsing information goes here at top level, not in a class

# For where the ply library is not in the same directory
# sys.path.insert(0, "../..")
import sys
sys.path.insert(0, ".")

# if sys.version_info[0] >= 3:
    # raw_input = input

tokens = [ 'NAME', 'NUMBER', 'COMMA', 'LPAREN', 'RPAREN' ] 

# literals = ['=', '+', '-', '*', '/', '(', ')']
literals = ['=', '+', '-', '*', '/', ]

# Tokens

t_NAME = r'[a-zA-Z_][a-zA-Z0-9_]*'

t_COMMA = r','
t_LPAREN = r'\('
t_RPAREN = r'\)'


def t_NUMBER(t):
    r'\d+'
    t.value = int(t.value)
    return t

t_ignore = " \t"


def t_newline(t):
    r'\n+'
    t.lexer.lineno += t.value.count("\n")


def t_error(t):
    error_stack.append("Illegal character '{}'".format(t.value[0]))
    t.lexer.skip(1)

# Parsing rules

precedence = (
    ('left', '+', '-'),
    ('left', '*', '/'),
    ('right', 'UMINUS'),
)

# Grammar rules

# Node types for the AST, if you change these, also update in __init__ 
N_APPLY = 'apply'
N_SET = 'set'
N_GET = 'get'
N_CONST = 'const'
N_PASS = 'pass'


# p_statement is the root of the resulting AST
def p_statement_expr(p):
    'statement : expression'
    p[0] = p[1]


def p_statement_empty(p):
    "statement : "
    p[0] = ValueTree(N_PASS)


def p_expression_assign(p):
    'expression : NAME "=" expression'
    p[0] = ValueTree(N_SET, [ ValueTree(p[1]), p[3] ])


def p_expression_binop(p):
    '''expression : expression '+' expression
                  | expression '-' expression
                  | expression '*' expression
                  | expression '/' expression'''
    p[0] = ValueTree(N_APPLY, [ ValueTree(p[2]), p[1], p[3] ])


def p_expression_uminus(p):
    "expression : '-' expression %prec UMINUS"
    p[0] = ValueTree(N_APPLY, [ValueTree("neg"), p[2] ])


def p_fn_apply_0(p):
    "expression : NAME LPAREN RPAREN"
    p[0] = ValueTree(N_APPLY, [ ValueTree(p[1]) ])


def p_fn_apply(p):
    "expression : NAME LPAREN expr_list RPAREN"
    p[0] = ValueTree(N_APPLY, [ ValueTree(p[1]) ] + p[3] )


def p_expression_group(p):
    "expression : LPAREN expression RPAREN"
    p[0] = p[2]


# Assemble elements of list, but delay ValueTree construction until 
# finish the list.

def p_expr_list_1(p):
    'expr_list : expression'
    p[0] = [ p[1] ]


def p_expr_list_2(p):
    'expr_list : expr_list COMMA expression'
    if p[1] is None:
        p[0] = p[3]
    else:
        p[0] = p[1] +  [p[3]]


def p_expression_number(p):
    "expression : NUMBER"
    p[0] = ValueTree(N_CONST, [ValueTree(p[1])])


def p_expression_name(p):
    "expression : NAME"
    p[0] = ValueTree(N_GET, [ValueTree(p[1])])

def p_error(p):
    if p:
        error_stack.append("Syntax error at '{}'".format(p.value))
    else:
        error_stack.append("Syntax error at EOF")

# Global error stack, on which we place results of calls to t_error, p_error
# If the stack is empty, the parse should be OK.
error_stack = []

from valueparser import ValueParser
class ExprParser(ValueParser):
    """
    Expression parser class. Returns a ValueTree representing the
    abstract syntax tree resulting from the parse. Each node in the ast
    with value ntype, and associated children, is interpeted as follows:

        const: [ value ] 
            - construct and return the constant value 

        set:  [ dest, src ] 
            - bind name dest to value src

        get: [ src ] 
            - fetch the value bound to name src

        apply: [ fn, args, ... ] 
            - apply the function fn to the arguments args 
            - not that things in the grammar, like binary ops +, *
            are also represented this way.

    """

    def __init__(self):
        """
        Parser object for simple expression language.

        In addition to the base class instance variables, this defines
        the following tables used to map symbols in the input grammar
        into 
        """
        # Note that we have to set up the references to the lexer and yacc 
        # parser here because the grammar is defined in this file scope.

        # Build the lexer
        import ply.lex as lex
        this_lexer = lex.lex()

        # Build the parser
        import ply.yacc as yacc
        this_yacc = yacc.yacc()

        # Link up the error stack
        this_error_stack = error_stack

        super().__init__(this_lexer, this_yacc, this_error_stack)

        # Node types for the AST, map from the name used in the
        # construction step of the rule, to the string that appears as
        # a value in the ValueTree that results from the parse.

        self.node_types = {
            'N_APPLY' : 'apply',
            'N_SET' : 'set',
            'N_GET' : 'get',
            'N_CONST' : 'const',
            'N_PASS' : 'pass',
            }


    def parse(self, input_str):
        # Invoke the initial parser in the base class.  

        (errors, ast) = super().parse(input_str)

        return (errors, ast)


    def unparse(self, t):
        """
        Unparse the AST that we have generated.
        """
        children = t.get_children()
        n = len(children)
        s = ""
        if n == 0:
            return str(t.get_value())

        op = self.fn_to_op.get(t.get_value()) 

        binary_op = (n == 2) and (op is not None)

        if op is None:
            # if no actual function, use the value in the expression tree
            op = t.get_value()

        # Special case for binary operations
        if binary_op:
            return "({} {} {})".format(
                self.unparse(children[0]), 
                op,
                self.unparse(children[1]))

        return "{}({})".format(op, 
            ",".join([self.unparse(c) for c in children]))


        
def tests():
    """
    Regression tests
    >>> p = ExprParser()

    >>> (e, t) = p.parse("(42)") 
    >>> e
    []
    >>> t.tree_to_valshape()
    ('const', [(42, [])])

    >>> (e, t) = p.parse("1 + 2") 
    >>> e
    []
    >>> t.tree_to_valshape()
    ('apply', [('+', []), ('const', [(1, [])]), ('const', [(2, [])])])

    >>> (e, t) = p.parse("x + 2") 
    >>> e
    []
    >>> t.tree_to_valshape()
    ('apply', [('+', []), ('get', [('x', [])]), ('const', [(2, [])])])

    >>> (e, t) = p.parse("f(1)") 
    >>> e
    []
    >>> t.tree_to_valshape()
    ('apply', [('f', []), ('const', [(1, [])])])

    >>> (e, t) = p.parse("f(1, 2, 3)") 
    >>> e
    []
    >>> t.tree_to_valshape()
    ('apply', [('f', []), ('const', [(1, [])]), ('const', [(2, [])]), ('const', [(3, [])])])

    >>> (e, t) = p.parse("f()") 
    >>> e
    []
    >>> t.tree_to_valshape()
    ('apply', [('f', [])])

    >>> (e, t) = p.parse("x = 1 + y") 
    >>> e
    []
    >>> t.tree_to_valshape()
    ('set', [('x', []), ('apply', [('+', []), ('const', [(1, [])]), ('get', [('y', [])])])])

    >>> (e, t) = p.parse("")
    >>> e
    []
    >>> t.tree_to_valshape()
    ('pass', [])

    >>> (e, t) = p.parse("(1,2)")
    >>> e
    ["Syntax error at ','"]
    >>> t.tree_to_valshape()
    ('pass', [])

    >>> (e, t) = p.parse("()+()")
    >>> e
    ["Syntax error at ')'"]
    >>> t.tree_to_valshape()
    ('pass', [])

    """

if __name__ == "__main__":
    import doctest
    doctest.testmod()
