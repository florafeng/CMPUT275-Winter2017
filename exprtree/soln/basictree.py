"""
BasicTree Class

Intent is to use this to represent any tree-like thing.

We think of a tree is being composed of subtrees, joined together
at the root.  A tree has-a list of children.

If the list of children is empty, we say the tree is empty.

An empty tree t is constructed by
    t = BasicTree() 

If t_0, t_1, ..., t_n are Trees, then 
    t = BasicTree([t_0, t_1, ..., t_n])
constructs a tree with the given subtrees as children.
Children are ordered, left to right, in same order as the list.

Question: During construction, Can t_i and t_j be the same tree?  

Maybe yes, maybe no, depending on how the tree is going to be used. If
it is immutable, then this structure sharing would be ok. If it can be
changed, then the children being passed must be "different" or
"independent", for some meaning of this.

Pre-condition:
    The children must be "independent".

Minimal doc tests

    >>> t = BasicTree()
    >>> t._children == []
    True

    >>> t = BasicTree([1])
    Traceback (most recent call last):
    ...
    ValueError: Not every child is-a <class '__main__.BasicTree'>

    >>> cl = [ BasicTree(), BasicTree() ]
    >>> t = BasicTree(cl)
    >>> t.get_children() == cl
    True

"""
__version__ = '1.0.2'


class BasicTree:

    """
    BasicTree class

    BasicTree(children) - create a new instance of the Tree class

    """

    def __init__(self, children=None):
        """
        This method is invoked when the Tree() constructor method
        is invoked to instantiate a new instance of class Tree.
        self is bound to the newly created bare object, and then
        __init__ initializes the initial state of the object.

        All objects contain a dictionary that is used to store its
        attributes (instance variables).  You access an instance
        variable x of object o by doing o.x 

        Inside a method, this is usually self.x

        By convention, _var names are private to the object. But
        you are not prevented from touching them from outside.
        """

        if children is None:
            self._children = []
        else:
            self._children = children

        # We should check on construction that the children are
        # really trees of the same type as self.

        if not all([ type(t) is type(self) for t in self._children ] ) :
            raise ValueError("Not every child is-a {}".format(type(self)))

        # And help guard against multiple cases of the same tree as a child.

        # Note: this may be difficult to do in a reliable way, but a little
        # warning is better than nothing.
        already_used = set()
        for i, c in enumerate(self._children):
            if c in already_used:
                raise ValueError(
                    "Duplicate child provided in argumner {} to constructor"
                    .format(i))
            already_used.add(c)

    # Accessor methods
    def get_children(self):
        """
        Return the children list of the tree - not a copy!
        """
        return self._children

    # Replace children
    def set_children(self, children):
        """
        Set the children list of the tree to the new list, releasing
        the old list of children.
        """
        self._children = children

    # Extract the shape as a list of lists
    def get_shape(self):
        """
        Returns a list of lists that has the same shape as the tree.
        For example, a tree and its shape list

        >>> t = BasicTree([BasicTree([BasicTree(), BasicTree()]), BasicTree()])
        >>> t.get_shape()
        [[[], []], []]

        For BasicTree this is the inverse to the list_to_tree class method.

        """
        return [ c.get_shape() for c in self.get_children() ]


    @classmethod
    def list_to_tree(Cls, l):
        """
        Generic tree constructor, that builds a tree with the same shape
        as the list l.  Sub lists correspond to non-empty children, and
        any element of l that is not a list generates an empty tree.

        Works for any class cls derived from BasicTree

        >>> s = []
        >>> s == BasicTree.list_to_tree(s).get_shape() 
        True

        >>> s = [[],[ [], [ [],[], [] ]]]
        >>> s == BasicTree.list_to_tree(s).get_shape() 
        True

        >>> v = [0,[ 1, [ 2, 3, 4]]]
        >>> s = [[],[ [], [ [],[], [] ]]]
        >>> s == BasicTree.list_to_tree(v).get_shape() 
        True

        >>> s = [[],[ [], [ [],[], [] ]]]
        >>> t_orig = BasicTree.list_to_tree(s)
        >>> t_copy = t_orig.list_to_tree(t_orig.get_shape())
        >>> t_copy.get_shape() == s
        True

        """

        # List of children we are assembling for this node, we construct
        # trees of class cls.
        clist = []
        for e in l:
            if type(e) is list:
                # if element is a list, construct the child tree
                clist.append(Cls.list_to_tree(e))
            else:
                # just a place holder for an empty tree
                clist.append(Cls())

        # Make a node with these children
        return Cls(children = clist)


if __name__ == "__main__":
    import doctest
    doctest.testmod()
