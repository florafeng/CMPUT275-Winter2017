"""
Python Data Structure Visualizer

This class is used to extract the structure graph of a Python data
structure and then generate a graphviz .dot file that can be used to
display the digraph structure.

For downloads of graphviz and the documentation etc, see
    http://www.graphviz.org/

Nodes in the digraph are objects. Each node is tagged with the type of
the associated object. An edge A -> B in the digraph, from object A to
object B indicates that the object A references the object B. That is,
some attribute (a name if you like) of object A is bound to object B.

Two kinds of structure descriptions are provided.

The detailed-object description preserves Python's everything is an
object principle. This means that there will be many links to the same
object, like the number 42.

The compact description folds atomic like objects into the label on the
node. So for example, rather than there being a link to 42 from the 4th
element of a list, the 4th element shows 42. If the element is not
atomic, then there will be a * in that posiiton and a link to the object
being referenced.

Once a structure is analyzed, you can build either or both styles of
description.  If the structure changes you need to re-analyze it in
order to capture any structural changes.  Changes in the value of atomic
objects will be reflected if you re-generate the description.

This is a typical use case if you are repeatedly dumping the .dot file
for graphviz to render as you step through an algorithm:

    from StructViz import *
    def update_dot(v, obj, basename, style='compact'):
        f = open(basename + '.dot', "w", encoding="utf-8")
        v.analyze_struct(obj)
        if style == 'compact':
            rep = v.gen_compact_dot_desc()
        else:
            rep = v.gen_detailed_dot_desc()
        f.write(rep)
        f.close()

Below we provide two interfaces for update_dot, one for the class,
one for a StructViz object instance

Minimal doc tests

    >>> v = StructViz()

    >>> obj = [1, '42', [2, 3] ]

    >>> v.analyze_struct(v)
    Traceback (most recent call last):
     ...
    ValueError: Cannot analyze yourself!

    >>> v.analyze_struct(obj)

    >>> full_object_desc = v.gen_detailed_dot_desc()

    >>> compact_desc = v.gen_compact_dot_desc()

"""
import re

__version__ = '1.0.1'


class StructViz:
    # StructViz classifies objects in these rough terms:

    # Atoms are not collections, so we don't descend into them for further
    # display.  This means that their values can be pushed up to enclosing
    # collections node when rendering, thus removing all kinds of edge noise.

    # NB - there is no built-in function type (eg like int), so we use
    # type(lambda x:x) to generate the type. We could also import the
    # types module and use the constant types.FunctionType

    atom_like = { type, type(None), type(lambda x: x),
        int, bool, float, complex, str }
    list_like = { list, tuple, set }
    dict_like = { dict }
    internal_like = { }

    # String used to indicate a reference link in the compact rep form.
    ref_char = "*"

    """
    The data structure is represented as a dict of nodes, keyed by
    object id. Each node is itself a dict with these fields:

    name - is the string name of the node to be used in creating
    the .dot file

    type - is the python type object that the node represents

    style - the style of node for display purposes
        'A' - singleton/atomic object, contents = None
        'L' - list-like object,
                contents = [ obj_id1, obj_id1, obj_id1, ... ]
              referencing the objects in position order
        'D' - dictionary like
                values = [ (key0, obj_id0), (key1, obj_id1), ... ]
              referencing the objects in position order
        'G' - some object with a __dict__ attribute,
        'I' - internal undisplayable object
        'U' - some unknown kind of object

    seqnum - the sequence number of the node as it is generated.
        used to improve the quality of the graphviz layout

    referers - is a list of all the other nodes that reference this
    one. Each referer is a (obj_id, pos) tuple where obj_id is the id
    of the object referencing this node, and pos is the position of
    the reference in the referring object collection. The position is 0 for
    non-collections, and an non-negative integer for collections.
    Hmm, a non collection cannot refer to an object?

    obj - ref to the actual object that this node is associated with

    contents - if non empty, it is a list of the object id's that
    are contained in this object, as a collection. The list of ids
    induces a position for the reference so that edges can be drawn
    from specific parts of the referencing collection to the
    referenced object.

    """

    def __init__(self):
        self._nodes = { }
        # the sequence number preserves the ordering of node generation,
        # this helps improve the layout if we give graphviz the nodes in
        # the same ordering.
        self._next_seqnum = 0

    def analyze_struct(self, obj):
        """
        Traverse the directed graph induced by the references inside
        the object obj.  During this traversal build up an internal
        model that will be used to render the graph in graphviz .dot
        format.
        """

        # Self analysis will recurse forever since analysis mutates the
        # thing being analyzed.
        if self is obj:
            raise ValueError("Cannot analyze yourself!")

        self.__init__()
        self.analyze_struct_r(obj, None)

    def analyze_struct_r(self, obj, referer):
        """
        Recurser associated with analyze_struct, not user called.
        """

        """
        We recursively walk the data structure by following all object
        references in the current object obj.

        Following a reference induces an edge in the digraph from the
        referring object to the referenced object. But the edge is not
        simple if the referring object is a collection. We also need to
        track what position the reference has in the collection in
        order to properly draw the links from the referer to the
        object. Thus the referer parameter is a tuple (name, pos) that
        is the name of the node, and the position in the collection,
        that references obj.

        This function thus does:
            - if this is the first encounter of obj, it assigns a name
            to obj and inserts a node into the _nodes attribute.
            - updates the node information with a link from referer to
            obj
            - returns the assigned name of obj

        """

        # The _nodes dict is indexed by object id. We use the string
        # version of the object id as a name. But we reserve the
        # capability to associate more meaningful names later.

        obj_id = id(obj)

        # If obj already visited, just add the referer information and
        # return the name associed with obj

        if obj_id in self._nodes:
            # Just add to the list of referers
            node = self._nodes[obj_id]
            if referer is not None:
                node['referers'].append(referer)
            return node['name']

        # Create and insert a node with the next sequence number

        name = str(obj_id)
        obj_type = type(obj)

        node = {
            'obj': obj,
            'name': name,
            'type': obj_type,
            'style': None,
            'seqnum': self._next_seqnum,
            'referers': [],
            'contents': None}

        self._nodes[obj_id] = node
        self._next_seqnum += 1

        # add the referring object, if any
        if referer is not None:
            node['referers'].append(referer)

        # Traversal stops at these atomic objects, so they will never be
        # a referer.
        if obj_type in StructViz.atom_like:
            node['style'] = 'A'
            return name

        # Enumerable list-like objects contain references, so we need to
        # build edges from the container obj to the items in the container.
        if obj_type in StructViz.list_like:
            node['style'] = 'L'
            node['contents'] = []
            for item_pos, item in enumerate(obj):
                item_name = self.analyze_struct_r(item, (obj_id, item_pos) )
                node['contents'].append( id(item) )
            return name

        # Dictionaries are list-like objects, but we want to sort them by
        # key value when we layout the node.
        if obj_type in StructViz.dict_like:
            node['style'] = 'D'
            # this
            #   for key, item in sorted(obj.items()):
            # does not work when keys are not orderable, for example
            # keys are a mix of tuples and strings.  So we try to do
            # a lexicographical sort, and if that fails we sort by the
            # string representation of the key.
            try:
                keys = sorted(obj.keys())
            except:
                keys = sorted(obj.keys(), key=str)

            node['contents'] = []
            for item_pos, key in enumerate(keys):
                item = obj[key]
                item_name = self.analyze_struct_r(item, (obj_id, item_pos) )
                node['contents'].append( (key, id(item) ) )

            return name

        # Some internal objects we don't want to inspect further.
        if obj_type in StructViz.internal_like:
            node['style'] = 'I'
            return name

        # Everything is an object, but some are more objectty than others.
        # Looks like an object if it has a __dict__ attribute
        if hasattr(obj, '__dict__'):
            node['style'] = 'G'
            # Same sorting trick as for dicts
            try:
                keys = sorted(obj.__dict__.keys())
            except:
                keys = sorted(obj.__dict__.keys(), key=str)

            node['contents'] = []
            for item_pos, key in enumerate(keys):
                item = obj.__dict__[key]
                item_name = self.analyze_struct_r(item, (obj_id, item_pos) )
                node['contents'].append( (key, id(item) ) )
            return name

        # It's some kind of object we don't handle
        node['style'] = 'U'
        return name

    def gen_detailed_dot_desc(self):
        """
        Generate a detailed description that preserves Python's
        "everything is an object" principle.

        Returns a string which when printed as the sole content of a .dot
        file can be processed by graphviz.
        """

        # Processing the nodes in the same order as they were generated,
        # then dumping all the nodes followed by all the edges seems to
        # produce the best layout by graphviz.

        # An edge is a 3-tuple (src_name, src_pos, dest_name)
        edges = [ ]

        # Result will be a string that is the .dot encoding of the graph

        # Start accumulating the description into the string result. We
        # could use the more efficient approach of generating a list of
        # lines and then joining them with newlines when # we are done.

        result = "\n".join( [
            "digraph structure {",
            "ordering=out;",
            "node [height=.1];",
            "rankdir=TB;",
            "" ] )

        # The key function is passed a (key,value) tuple.  This will sort
        # by sequence number.
        by_seqnum = lambda k: k[1]['seqnum']

        for key, node in sorted(self._nodes.items(), key=by_seqnum):
            # Extract the fields of the node record
            obj = node['obj']
            name = node['name']
            obj_type = node['type']
            style = node['style']
            referers = node['referers']
            contents = node['contents']

            # Construct the referring edges for this node
            for (src_name, src_pos) in referers:
                edges.append( (src_name, src_pos, name) )

            node_type = StructViz.esc_dot_specials(str(obj_type))

            # Now create a graphviz node according to the style of this node

            if style == 'A':
                v = StructViz.format_value(obj)
                result += (
                    '{} [shape=polygon, sides=4, peripheries=1, '
                    'label="{}\n{}" ]\n'
                    ) . format(name, node_type, v)

            elif style == 'L':
                # A .dot record label looks like this, where the <f0> are
                # tags so that the edges exit from specific parts of the
                # node:
                #   name [label="<f0> | <f1> value | <f2>"];
                # So you can see why escaping the specials is important!

                items = []
                for i, e in enumerate(contents):
                    items.append( '<f{}> {}' . format(i, i) )

                fields = ' | ' . join(items)

                result += (
                    '{} [shape=record, height=.1, '
                    'label="{{ {} | {{ {} }} }}"];\n'
                    ) .  format(name, node_type, fields)


            # Dictionaries, including objects with __dict__
            elif style in { 'D', 'G' }:
                items = []
                for i, (key, e) in enumerate(contents):
                    items.append(
                        '<f{}> {}' . format(i, StructViz.format_value(key)) )

                fields = ' | ' . join(items)
                result += (
                    '{} [shape=record, height=.1, '
                    'label="{{ {} | {{ {} }}   }}"];\n'
                    ) . format(name, node_type, fields)

            # Internal implementation objects
            elif style in { 'I' }:
                result += (
                    '{} [shape=polygon, sides=4, peripheries=2, '
                    'label="{}" ]\n'
                    ) . format(name, node_type)

            # Other kinds of objects
            else:
                result += (
                    '{} [shape=polygon, sides=4, peripheries=2, '
                    'label="{}\n{}" ]\n'
                    ) . format(name, node_type, 'Not Implemented')

        # dump edges
        for e in edges:
            (src_name, src_pos, dest_name) = e
            result += ( '{}:<f{}> -> {};\n'
                ) . format(src_name, src_pos, dest_name )

        result += "}\n"
        return result

    def gen_compact_dot_desc(self):
        """
        Generate a compact description to make for smaller and simpler
        diagrams at the expense of object referencing accuracy.

        Returns a string which when printed as the sole content of a .dot
        file can be processed by graphviz.
        """

        # See the comments in gen_detailed_dot_desc as the processing is
        # similar.

        # An edge is a 3-tuple (src_name, src_pos, dest_name)
        edges = [ ]

        # Result will be a string that is the .dot encoding of the graph.

        result = "\n".join( [
            "digraph structure {",
            "ordering=out;",
            "node [height=.1];",
            "rankdir=TB;",
            "" ] )

        # The key function is passed a (key,value) tuple.  This will sort
        # by sequence number.
        by_seqnum = lambda k: k[1]['seqnum']

        for key, node in sorted(self._nodes.items(), key=by_seqnum):
            # Extract the fields of the node record
            obj = node['obj']
            name = node['name']
            obj_type = node['type']
            style = node['style']
            referers = node['referers']
            contents = node['contents']

            node_type = StructViz.esc_dot_specials(str(obj_type))

            # Construct the referring edges for this node only if it is
            # not an atom, in which case it will have been moved up into
            # the container
            if style != 'A':
                for (src_name, src_pos) in referers:
                    edges.append( (src_name, src_pos, name) )


            # Now create a graphviz node according to the style of this node

            if style == 'A':
                # The special case of no referers means the atomic value cannot
                # be folded back into the container node.  So it has to have
                # it's own node
                if len(referers) == 0:
                    v = StructViz.format_value(obj)
                    result += (
                        '{} [shape=polygon, sides=4, peripheries=1, '
                        'label="{}" ]\n'
                        ) . format(name, v)

            elif style == 'L':
                # A .dot record label looks like this, where the <f0> are
                # tags so that the edges exit from specific parts of the
                # node:
                #   name [label="<f0> | <f1> value | <f2>"];
                # So you can see why escaping the specials is important!

                items = []
                for i, e in enumerate(contents):
                    e_node = self._nodes[e]
                    if e_node['style'] == 'A':
                        v = StructViz.format_value(e_node['obj'])
                    else:
                        v = StructViz.ref_char

                    items.append( '<f{}> {}\\n{}' . format(i, i, v) )

                fields = ' | ' . join(items)

                result += (
                    '{} [shape=record, height=.1, '
                    'label="{{ {} | {{ {} }} }}"];\n'
                    ) .  format(name, node_type, fields)


            # Dictionaries, including objects with __dict__
            elif style in { 'D', 'G' }:
                items = []
                for i, (key, e) in enumerate(contents):
                    e_node = self._nodes[e]
                    if e_node['style'] == 'A':
                        v = StructViz.format_value(e_node['obj'])
                    else:
                        v = StructViz.ref_char

                    items.append( (
                        '<f{}> {}\\n{}'
                        ) . format(i, StructViz.format_value(key), v) )

                fields = ' | ' . join(items)
                result += (
                    '{} [shape=record, height=.1, '
                    'label="{{ {} | {{ {} }}   }}"];\n'
                    ) . format(name, node_type, fields)

            # Internal implementation objects
            elif style in { 'I' }:
                note = ''
                result += (
                    '{} [shape=polygon, sides=4, peripheries=2, '
                    'label="{}\\n{}" ]\n'
                    ) . format(name, node_type, note)

            # Other kinds of objects
            else:
                note = ''
                result += (
                    '{} [shape=polygon, sides=4, peripheries=2, '
                    'label="{}\n{}" ]\n'
                    ) . format(name, node_type, note)

        # dump edges
        for e in edges:
            (src_name, src_pos, dest_name) = e
            result += ( '{}:<f{}> -> {};\n'
                ) . format(src_name, src_pos, dest_name )

        result += "}\n"
        return result

    
    def update_dot(self, obj, basename, 
        style='compact', pause=0, format=None):

        """

        obj - object to be vizualized
        
        basename - base name of the output file, if missing is called
            viz.  Output file is <basename>.dot

        style - 'compact', 'detailed' - style of output.

        pause - the amount of time to sleep after updating the drawing.  
            0 means no delay
            >0 means delay in seconds
            <0 means wait for user to provide a line (ignored) on stdin 
               before proceeding

        format - a list of options containing: pdf, png
            after generating the output file, render it into the appropriate
            specified formats, which will be placed in
                "graph.dot.pdf" "graph.dot.png"
            if the file name is "graph.dot".
        """

        file_name = basename + '.dot'
        f = open(file_name, "w", encoding="utf-8")
        self.analyze_struct(obj)
        if style == 'compact':
            rep = self.gen_compact_dot_desc()
        else:
            rep = self.gen_detailed_dot_desc()
        f.write(rep)
        f.close()

        # Enable this to generate png
        if format is not None:
            if "png" in format:
                import subprocess
                subprocess.call(["dot", "-Tpng", file_name, "-O"])

            if "pdf" in format:
                import subprocess
                subprocess.call(["dot", "-Tpdf", file_name, "-O"])

        # wait for user to proceed
        if pause < 0: 
            s = input('\n<CR> to continue')
        elif pause > 0:
            time.sleep(pause)

    @classmethod
    def update_viz(cls, obj, basename, style='compact', pause=0, format=None):
        v = StructViz()
        v.update_dot(obj, basename, style, pause, format)

    @staticmethod
    def format_value(v):
        """
        Given an object v that is sort of atomic, convert its value into
        a string form in which all characters special to .dot syntax are
        escaped. So far the special handling we do is:

            None is converted to string 'None'
            ' ' is placed around strings to indicate their stringness
            numbers are converted to strings
            types and tuples are converted to strings (tuples should be
                short)
            anything else is represented as type plus object id.

        Then the final result is processed to escape any special .dot file
        characters.
        """

        if v is None:
            return 'None'

        if type(v) in { int, bool, float, complex }:
            # These have safe string representations
            return StructViz.esc_dot_specials( str(v) )

        if type(v) == str:
            # Put ' ' around to string to make it clear it's a string
            return StructViz.esc_dot_specials( "'" + v + "'")

        if type(v) in { tuple, type }:
            # We are ok with the string rep of these, under the assumption
            # that the tuple is small.
            return StructViz.esc_dot_specials( str(v) )

        # Any thing else doesn't have an obvious representation, so
        # display as its type and object id.  Put the id under the 
        # type so that it is more compact.
        # was:
        # return StructViz.esc_dot_specials(
        #    str(type(v)) + '\\n' + str(id(v)) )
        return StructViz.esc_dot_specials(
            str(type(v))) + '\\n' + StructViz.esc_dot_specials(str(id(v)))

    @staticmethod
    def esc_dot_specials(v):
        """
        Escape each of the following chars <>|[]\;{} that are used
        by a .dot file for the label descriptions.
        """

        # Oh I yearn for the ease of Perl regexps. But Python does have
        # a nice format method.

        r = re.sub(r'[<>"|[\]\\{};]', (lambda m: "\\" + m.group(0)), v)
        return r


if __name__ == "__main__":
    import doctest
    doctest.testmod()
