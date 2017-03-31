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


"""
__version__ = '1.0.2'


class BasicTree:

    """
    BasicTree class

    BasicTree(children) - create a new instance of the Tree class

Minimal doc tests

    >>> t = BasicTree()
    >>> t._children == []
    True

    >>> cl = [ BasicTree(), BasicTree() ]
    >>> t = BasicTree(cl)
    >>> t.get_children() == cl
    True

    >>> t1 = BasicTree()
    >>> t2 = BasicTree([t1, 42])
    Traceback (most recent call last):
    ...
    ValueError: Children in positions 1 are not of class <class '__main__.BasicTree'>

    >>> t2 = BasicTree([[], t1, []])
    Traceback (most recent call last):
    ...
    ValueError: Children in positions 0,2 are not of class <class '__main__.BasicTree'>

    >>> t2 = BasicTree([t1, t1])
    Traceback (most recent call last):
    ...
    ValueError: Duplicate children in positions 1

    >>> t1.set_children([1])
    Traceback (most recent call last):
    ...
    ValueError: Children in positions 0 are not of class <class '__main__.BasicTree'>

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
            self.check_children(children)
            self._children = children

    def check_children(self, children):
        """
        Check that children are roughly compliant with the assumption that
        they are instances of the class being constructed, and unique 
        identities.
        """


        bad_class_positions = []
        duplicate_positions = []

        already_used = set()
        for i, c in enumerate(children):

            # Is this child the same class as self?
            # Do we instead allow any subclass of self?

            if type(c) is not type(self):
                bad_class_positions.append(i)

            # And help guard against multiple cases of the same tree as a child.
            # Note: this is difficult to do in a reliable way, but a little
            # warning is better than nothing.

            if id(c) in already_used:
                duplicate_positions.append(i)
            else:
                already_used.add(id(c))

        if len(bad_class_positions) > 0:
            raise ValueError("Children in positions {} are not of class {}".
                format(",".join(map(str, bad_class_positions)), type(self)))

        if len(duplicate_positions) > 0:
            raise ValueError("Duplicate children in positions {}".
                format(",".join(map(str, duplicate_positions))))

        return True

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
        self.check_children(children)
        self._children = children

    # Extract the shape as a list of lists
    def tree_to_shape(self):
        """
        Returns a list of lists that has the same shape as the tree.
        For example, a tree and its shape list

        >>> t = BasicTree([BasicTree([BasicTree(), BasicTree()]), BasicTree()])
        >>> t.tree_to_shape()
        [[[], []], []]

        For BasicTree this is the inverse to the shape_to_tree class method.

        """
        return [ c.tree_to_shape() for c in self.get_children() ]


    @classmethod
    def shape_to_tree(cls, l):
        """
        Generic tree constructor, that builds a tree with the same shape
        as the list l.  Sub lists correspond to non-empty children, and
        an empty list generates an empty tree.

        Works for any class cls derived from BasicTree

        >>> s = []
        >>> s == BasicTree.shape_to_tree(s).tree_to_shape() 
        True

        >>> s = [[],[ [], [ [],[], [] ]]]
        >>> s == BasicTree.shape_to_tree(s).tree_to_shape() 
        True

        >>> s = [[],[ [], [ [],[], [] ]]]
        >>> t_orig = BasicTree.shape_to_tree(s)
        >>> t_copy = t_orig.shape_to_tree(t_orig.tree_to_shape())
        >>> t_copy.tree_to_shape() == s
        True

        """

        # List of children we are assembling for this node, we construct
        # trees of class cls.
        children = []
        for e in l:
            if type(e) is list:
                # if element is a list, construct the child tree
                children.append(cls.shape_to_tree(e))
            else:
                raise ValueError("Non list element '{}'".format(e))

        # Make a node with these children, the children paramater may
        # be in different position for the cls() constructor, so specify it.
        return cls(children = children)


if __name__ == "__main__":
    import doctest
    doctest.testmod()
