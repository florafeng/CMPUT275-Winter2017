"""
Parser for simple logical formula

Instead of generating the parse tree, actually evaluates the formula,
and returns the value True or False.  If the formula has a variable in
it, it can't be evaluated, so an exception is generated instead.

"""

from valuetree import ValueTree

# Parsing information goes here at top level, not in a class

# For where the ply library is not in the same directory
# import sys
# sys.path.insert(0, "../..")

# if sys.version_info[0] >= 3:
    # raw_input = input

tokens = [ 'ID', 'AND', 'OR', 'NOT', 'TRUE', 'FALSE', 'LPAREN', 'RPAREN' ]

literals = [ ]

# Tokens

t_ID = r'[a-z]'
t_AND = r'&'
t_OR = r'\|'
t_NOT = r'~'
t_TRUE = r'T|1'
t_FALSE = r'F|0'
t_LPAREN = r'\('
t_RPAREN = r'\)'

t_ignore = " \t"

def t_newline(t):
    r'\n+'
    t.lexer.lineno += t.value.count("\n")

def t_error(t):
    error_stack.append("Illegal character '{}'".format(t.value[0]))
    t.lexer.skip(1)

# Parsing rules

precedence = (
    ('left', 'OR'),
    ('left', 'AND'),
    ('right', 'NOT'),
)

# Grammar rules
# Associate with each rule is code that builds the result of applying
# the rule - it's attribute.
# The parts of the rule come in as items 1, 2, ... k of the list p
# corresponding to the position in the production. The value of the part
# depends on how the part itself was constructed.

# In this example, we actually generate a syntax tree to show the structure
# of the expression.  It directly follows the order in the production.

# p_expression is the root of the resulting AST
def p_expression(p):
    '''expression : expression_false
        | expression_true'''
    p[0] = p[1]

def p_expression_true(p):
    '''expression_true : TRUE
        | expression_true AND expression_true
        | expression_true OR expression_true
        | expression_true OR expression_false
        | expression_false OR expression_true
        | NOT expression_false
        | LPAREN expression_true RPAREN'''
    p[0] = True
    # p[0] = [ '1' ]

def p_expression_false(p):
    '''expression_false : FALSE
        | NOT expression_true
        | expression_false AND expression_false
        | expression_true AND expression_false
        | expression_false AND expression_true
        | expression_false OR expression_false
        | LPAREN expression_false RPAREN'''
    p[0] = False
    # p[0] = [ '0' ]

def p_expression_id(p):
    '''expression : ID'''
    # p[0] = None
    raise ValueError("Expression has a variable '{}' in it".format(p[1]))

# def p_expression_binop(p):
#     '''expression : expression AND expression
#                   | expression OR expression'''
#     p[0] = [ "(", p[1], p[2], p[3], ")" ]
#

# def p_expression_not(p):
#     "expression : NOT expression %prec NOT"
#     p[0] = [ p[1], p[2] ]
#
#
# def p_expression_group(p):
#     "expression : LPAREN expression RPAREN"
#     p[0] = [ p[1], p[2], p[3] ]


def p_error(p):
    if p:
        error_stack.append("Syntax error at '{}'".format(p.value))
    else:
        error_stack.append("Syntax error at EOF")

# Global error stack, on which we place results of calls to t_error, p_error
# If the stack is empty, the parse should be OK.
error_stack = []

from valueparser import ValueParser
class LogicParser(ValueParser):
    """
    Parse for Boolean expressions
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

    def parse(self, input_str):
        # Invoke the initial parser in the base class.
        # The parser in this case can raise an exception, so capture it.

        errors = []
        ast = None
        try:
            (errors, ast) = super().parse(input_str)
        except ValueError as e:
            errors = [ e ]

        return (errors, ast)


    def unparse(self, t):
        """
        Unparse the AST that we have generated.
        """
        pass

def do_test(s):
    """
    Helper function for doc test generation
    """
    (errors, ast) = parser.parse(s)
    return (errors, ast)

def tests():
    """
    Regression tests

    >>> do_test("1")
    ([], True)

    >>> do_test("T")
    ([], True)

    >>> do_test("0")
    ([], False)

    >>> do_test("F")
    ([], False)

    >>> do_test("x")
    ([ValueError("Expression has a variable 'x' in it",)], None)

    >>> do_test("1 & 0")
    ([], False)

    >>> do_test("1 | 0")
    ([], True)

    >>> do_test("~ 1")
    ([], False)

    >>> do_test("( ( ~ 1 ) ) ")
    ([], False)

    >>> do_test("1 & 0 | 1 & 1 | 0 | 1")
    ([], True)

    >>> do_test("1 & ~ 0 | ~ ~ 1 & 1 | 0 | 1")
    ([], True)

    >>> do_test("x & ~ y | ~ ~ z & t | u | v")
    ([ValueError("Expression has a variable 'x' in it",)], None)

    """

parser = LogicParser()
def main():
    from structviz import StructViz
    viz_format = [ 'png' ]


    # Ask for an expression until get EOF or blank line.
    # Note use of next, instead for s in sys.stdin:

    while True:
        print("?", end='', flush=True)
        # return empty string on EOF
        s = next(sys.stdin, "")
        s = s.strip()
        if s == "":
            # Quit on blank line or EOF
            break

        (errors, ast) = parser.parse(s)

        if len(errors) > 0:
            print("Errors:")
            for e in errors:
                print(e)

        print("Result:", ast)
        if False:
            StructViz.update_viz(ast, "t-ast",
                style='compact', pause=0, format=viz_format)

        # Back for more

    print("Done")

def _test():
    import doctest
    doctest.testmod()

if __name__ == "__main__":
    """
    Doctest non-module execution
      python3 expr.py --test

    Run doctests if the --test argument is in command line arguments
    when run as a main program.

    Otherwise, run as a normal program.
    """

    import sys
    if "--test" in sys.argv:
        print("Running doctests")
        _test()
        exit()

    # Start the compiler
    main()
