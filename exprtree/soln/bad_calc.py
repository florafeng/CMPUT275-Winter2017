import sys
sys.path.insert(0, "../lib")

"""
Calculator that uses expression trees, but implements all kind of
stuff outside the ExprTree class
"""

from exprtree import *

# map from operator to the function that computes it.  We use lambda
# expressions to enable the table to be inverted - since each lambda is
# unique, the table is 1-1 and we can look up the operator symbol corresponding
# to the function.
op_to_fn = {
    'neg' : (lambda x : -x),
    '+' : (lambda x, y: x + y),
    '-' : (lambda x, y: x - y),
    '*' : (lambda x, y: x * y),
    }

fn_to_op = dict(
    [ (v, k) for k, v in op_to_fn.items() ]
    )


def list_to_expr_tree(l):
    """
    Convert the list form parse tree into a corresponding expression tree

    For example, 
        1 + ( 2 * 3 ) + 5
    parses into this list
        ['+', ['+', 1, ['*', 2, 3]], 5]

    """

    if type(l) is not list:
        # We have a constant
        return ExprTree(l)

    # We have an operation, convert the operation string, e.g. '+'
    # to its associated function, and store that as the value.  The
    # children are converted from their corresponding sub-expression

    # get corresponding function from table, None if not present.

    op = l[0]
    fn = op_to_fn.get(op)

    if fn is None:
        raise ValueError("Unimplemented operation '{}'".format(op))
        return ExprTree(None)

    return ExprTree(fn, [ list_to_expr_tree(term) for term in l[1:] ])

def main():

    from parse_expr import ExprParser

    # Input an expression, parse it into a nested-list parse tree,
    # conver to an expression tree, and then evaluate it.

    # Build a parser
    p = ExprParser()

    # Ask for an expression until get empty string
    while True:
        s = input("?")
        s = s.strip()
        if s == "": 
            break

        # Parse the expression into a nested-list parse tree
        l = p.parse(s)

        print("Parsed expr: {}".format(l))

        # Try to convert that list into an ExprTree

        convert_ok = True
        try:
            t = list_to_expr_tree(l)
        except ValueError as e:
            print("Bad conversion: {}".format(e))
            convert_ok = False

        # If we converted ok, then try to evaluate the expression

        if convert_ok:
            # for visualization purposes
            if False:
                file_name = "t"
                print("Resulting ExprTree in '{}.dot' and '{}.dot.png'".
                    format(file_name, file_name))
                disp = { 'op_to_fn' : op_to_fn, 'expr' : t }

                StructViz.update_viz(disp, file_name, 
                    style='compact', pause=0, format=['png'])

            try:
                r = t.evaluate()
                print("Result is {}".format(r))
            except Exception as e:
                print("Evaluation error: {}".format(e))

        # Go back for another expression


    print("Done")

main()
