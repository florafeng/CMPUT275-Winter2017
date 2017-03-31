"""
ValueTree Class

Extension of BasicTree to have a value associated with each node of 
the tree.

"""
from basictree import BasicTree
class ValueTree(BasicTree):

    """
    ValueTree class

    A ValueTree is an attributed BasicTree.  Each node of the tree has an
    associated value.

    ValueTree(v) - constructs a new instance, with value v and no
    children. It is a leaf.

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


    # Extract the shape as a list of lists
    def tree_to_valshape(self):
        """

        A valshape (value shape) is a representation of the the tree that
        describes both the shape and value attributes of the tree.

        Base case:  If t = ValueTree(v), then 
            t.tree_to_valshape() is the tuple (v, [])

        Inductive construction: If c = [t_0, ..., t_n] are ValueTree, and 
        t = ValueTree(v, c), then
            t.tree_to_valshape() is the tuple (v, [ vs_0, ..., vs_n ]) 
            where vs_i is the valshape of child t_i.
            
        >>> t = ValueTree(1, [ValueTree(2, [ValueTree(3), ValueTree(4)]), ValueTree(5)])
        >>> t.tree_to_valshape()
        (1, [(2, [(3, []), (4, [])]), (5, [])])

        Note that if the values in the tree have string representations,
        then value shapes can be used to save and load value trees on
        string-based storage.
        

        """
        return (self.get_value(), 
            [ c.tree_to_valshape() for c in self.get_children() ] )


    @classmethod
    def valshape_to_tree(cls, r):
        """

        Suppose t is a ValueTree, with valshape vs = t.tree_to_valshape(), 
        then 
            t_new = ValueTree.valshape_to_tree(vs)
        is a new ValueTree with the same shape and attributes as t.

        Works for any class cls derived from ValueTree

        >>> s = (42, [])
        >>> s == ValueTree.valshape_to_tree(s).tree_to_valshape() 
        True

        >>> s = (1, [(2, []),(3, [ (4, []), (5, [ (6, []),(7, []), (8, []) ])])])
        >>> s == ValueTree.valshape_to_tree(s).tree_to_valshape() 
        True

        >>> t_orig = ValueTree.valshape_to_tree(s)
        >>> t_copy = t_orig.valshape_to_tree(t_orig.tree_to_valshape())
        >>> t_copy.tree_to_valshape() == s
        True

        """

        (v, l) = r

        # List of children we are assembling for this node, we construct
        # trees of class cls.
        children = []
        for e in l:
            if type(e) is tuple:
                # if element is a list, construct the child tree
                children.append(cls.valshape_to_tree(e))
            else:
                raise ValueError("Element '{}' not in (value, childre)".format(e))

        # Make a node with these children, the children paramater may
        # be in different position for the cls() constructor, so specify it.
        return cls(value = v, children = children)


if __name__ == "__main__":
    import doctest
    doctest.testmod()
