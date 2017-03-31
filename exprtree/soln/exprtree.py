"""
ExprTree Class

General Expression Tree

"""
from valuetree import ValueTree

# If you need some utility functions for the class, just put them here
# and they can be called from the class.
op_to_fn = {
    'neg' : (lambda x : -x),
    '+' : (lambda x, y: x + y),
    '-' : (lambda x, y: x - y),
    '*' : (lambda x, y: x * y)
}

fn_to_op = dict(
    [ (v, k) for k, v in op_to_fn.items() ]
)

def list_to_expr_tree(l):
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


class ExprTree(ValueTree):

    """
    Expression tree.

    An expression tree is a ValueTree where the values in the tree are
    interpreted as follows:

    leaf nodes - have a value that is a constant object (e.g.
        number, string, etc.)

    internal nodes - have a value that is a function object, which takes
        the evaluated values of the children as its arguments.

    For example

    >>> t = ExprTree( lambda x, y: x + y, [ ExprTree(3), ExprTree(4) ] )
    >>> t.evaluate()
    7

    """

    def __init__(self, value=None, children=None):

        # The parent (super) class needs to be initialized.  It will
        # check the children for consistency
        super().__init__(value, children)

    # Expression-related operations

    def evaluate(self):
        # No children, return the value.  Hmm, maybe having an is_empty()
        # method would be useful.

        cl = self.get_children()
        if len(cl) == 0:
            return self.get_value()

        args = [ c.evaluate() for c in cl ]

        oper = self.get_value()

        # * is the special "use list as remaining parameters" operator
        # if f(x, y, z) takes three arguments, and args = [1, 3, 5]
        # then f(*args) is the same as f(1, 3, 5)

        return oper(*args)

    def unparse(self):
        """
        >>> t = ExprTree.parse("1 + (3 * 4)")
        >>> t.unparse()
        '(1 + (3 * 4))'

        """
        val = self.get_value()
        child = self.get_children()
        if len(child) == 0:
            str_rep = "{}".format(val)
        elif len(child) == 1:
            if fn_to_op[val] == 'neg':
                str_rep = "({} {})".format('-', child[0].unparse())
            # str_rep = "{} {}".format(fn_to_op[val], child[0].unparse())
        elif len(child) > 0:
            str_rep = "({} {} {})".format(child[0].unparse(), fn_to_op[val], child[1].unparse())

        # str_rep = ""
        # "({} {} {})".format(unparse(child[0], fn_to_op[tmp], unparse(child[0])
        return str_rep


    # This will hold the single instance of the parser
    parser = None

    @classmethod
    def parse(Cls, s):
        """
        Parse the string s into an ExprTree

        >>> t= ExprTree.parse("1 + 2")

        """

        from parse_expr import ExprParser

        # Create a singleton instance of the parser.
        if ExprTree.parser is None:
            ExprTree.parser = ExprParser()

        # dummy result
        t = ExprTree()
        s = s.strip()

        # Build a parser
        p = ExprParser()

        # Parse the expression into a nested-list parse tree
        l = p.parse(s)
        # print("Parsed expr: {}".format(l))
        m = list_to_expr_tree(l)

        return m


if __name__ == "__main__":
    import doctest
    doctest.testmod()
    # t = ExprTree.parse('((1 + 3) * (4 + 5))')
    # m = ExprTree.parse('14')
    # t.unparse()
