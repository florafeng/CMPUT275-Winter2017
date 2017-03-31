"""
ValueTree Class

Extension of BasicTree to have a value associated with each node of 
the tree.

"""
from basictree import BasicTree
class ValueTree(BasicTree):

    """
    ValueTree class

    Each tree has a value, and 0 or more sub-trees called children.

    ValueTree(v) - constructs a new instance of the Tree class, with value
        v and no children.  It is a leaf.

    If each of t0, t1, ..., tn is-a ValueTree, then 
        t = ValueTree(v, [t0, t1, ..., tn] )
    constructs a new tree with value v, and children t0, t1, ..., tn
    It is an internal node.

    """

    def __init__(self, value=None, children=None):

        # The parent (super) class needs to be initialized.  It will
        # check the children for consistency
        super().__init__(children)

        # Now us
        self._value = value

    # Accessors
    def get_value(self):
        return self._value

    def set_value(self, v):
        self._value = v


if __name__ == "__main__":
    import doctest
    doctest.testmod()
