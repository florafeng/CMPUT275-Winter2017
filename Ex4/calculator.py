import sys

"""
Simple expression-based calculator, with variables.  The expression
language is pecisely defined by the ExprParser class.  But in 
general it is the usual arithmetic formulas, with the additional
ability to bind variable names to values, and use the value a variable is 
bound to.
"""

from structviz import StructViz
from exprparser import ExprParser

# Debugging and comprehension settings
debug = True
visualize = True

# Extra output formats for structure visualizer
# viz_format = ['png'] 
# viz_format = ['pdf'] 
# viz_format = ['png', 'pdf'] 
viz_format = [] 

class Calculator():
    """
    A Calculator is a service for evaluating sequences of strings that
    represent formulas.  The formulas are evaluated in a context that
    provides a binding from variables to values, and formulas can change
    the context for later use.
    """

    def __init__(self):
        """
        Build an expression parser to get the AST for the input string

        Side Effect:
        This will generate, if not present and up-to-date, the parse 
        tables: 
            parser.out, parsetab.py
        in the current directory.
        """

        self.parser = ExprParser()


    # Tables mapping operators in the AST to corresponding functions during
    # evaluation, and vice-versa.
    op_to_fn = {
        'neg': (lambda x: -x),
        '+': (lambda x, y: x + y),
        '-': (lambda x, y: x - y),
        '*': (lambda x, y: x * y),
        '/': (lambda x, y: x / y),
        'sqr': (lambda x: x * x),
        '?': None,
        }

    fn_to_op = dict([(v, k) for k, v in op_to_fn.items()])

    def evaluate(self, expr_str, var_dict = None):
        """
        Evaluate the expression given by expr_str, using and updating the
        context defined by the variable dictionary var_dict.

        Inputs:
            expr_str - a string in the expression language
            var_dict - a dictionary that maps variable names to values

        Outputs:
            returns the value of the expression, or throws an exception
                containing parsing or evaluation errors.

            var_dict - updates the variable dictionary.  If an expression
                is partially evaluated and has modified variables in 
                var_dict, then if an error is encountered, the modifications
                will remain.

        """

        # Evaluation proceeds in two steps.  First parse the string into
        # and AST, represented by a ValueTree.  
        # Then traverse the AST evaluating it as an expression.

        try:
            (errors, ast) = self.parser.parse(expr_str)
        except Exception as e:
            raise ValueError( "Parseing internal error: {}".format(e))

        if len(errors) > 0:
            raise ValueError( "Parsing generated errors:\n{}".format(
                    "\n".join(errors)))

        if ast is None:
            return None

        if var_dict is None:
            var_dict = {}

        if debug:
            print(ast.tree_to_valshape())

        if visualize:
            StructViz.update_viz(ast, "t-ast",
                style='compact', pause=0, format=viz_format)

        return self.evaluate_ast(ast, var_dict)


    def evaluate_ast(self, ast, var_dict):
        """
        Traverse the AST, represented by a ValueTree, and evaulate it,
        using the appropriate functions as defined by op_to_fn.

        Examples:
            1 + 2
        =>
            ('apply', [('+', []), ('const', [(1, [])]), ('const', [(2, [])])])

        
            y = x + 1
        =>
            ('set', [('y', []), ('apply', [('+', []), 
                ('get', [('x', [])]), ('const', [(1, [])])])]

            (x = 2) + 1
        =>
            ('apply', [('+', []), ('set', [('x', []), 
                ('const', [(2, [])])]), ('const', [(1, [])])])

        """

        ntype = ast.get_value()
        children = ast.get_children()

        if ntype == 'const':
            return children[0].get_value()

        if ntype == 'apply':
            op = children[0].get_value()
            fn = self.op_to_fn.get(op)

            if fn is None:
                raise ValueError(
                    "Evaluation error, no implementation of operation '{}'".
                    format(op))

            args = [ self.evaluate_ast(c, var_dict) for c in children[1:] ]
            return fn(*args)
        
        if ntype == 'set':
            # bind name to value
            name = children[0].get_value()
            value = self.evaluate_ast(children[1], var_dict)
            var_dict[name] = value
            return value

        if ntype == 'get':
            # get value bound to name
            name = children[0].get_value()
            if name not in var_dict:
                raise ValueError(
                    "Evaluation error, variable '{}' has no value yet".
                    format(name))

            value = var_dict.get(name)
            return value

        # anything else
        raise ValueError(
            "Evaluation internal error, AST node type '{}' not implemented".
            format(ntype))


def main():

    # Persistent map of names to their current value
    var_dict = {}


    calc = Calculator()

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

        result = None
        try:
            result = calc.evaluate(s, var_dict)
        except Exception as e:
            print("Error: {}".format(e))

        print(result)

        # Back for more

    print("Done")

if __name__ == "__main__":
    # Start the calculator
    main()
