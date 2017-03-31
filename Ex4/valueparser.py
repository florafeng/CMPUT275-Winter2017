class ValueParser():
    """
    Base class of parsers that return ValueTrees as abstract syntax trees,
    also called ASTs, or parse trees.

    A parser object is composed of a lexer component and a yacc component.
    The lexer component converts the input string into lexical tokens.  
    The yacc component parses a stream of lexical tokens into a ValueTree
    representation of the AST.

    In general, an AST is just an attributed tree, which will usually
    require further processing to produce executable code (for the
    various meanings of "executable code"). Since a given parse tree can
    be used to generate various artifacts, that "code generation" step
    does not belong in this class hierarchy.

    The particular details of the grammar are given in the derived
    class, which contains the grammar (in ply format)

    We are using ply as the parser generator, developed by David Beazley
    and many collaborators. See: http://www.dabeaz.com/ply/

    But any tool with a lex and yacc style of interface would workC,
    including a pythone wrapper for the traditional C-based lex/yacc,
    flex/bison, or multu-lingual ANTLR etc. generators.

    Each parser has a parse method, and a a possibly unimplemented
    unparse method.

    """

    def __init__(self, lexer, yacc, error_stack):
        """
        The derived class constructs the lexer and parser, and creates
        the error_stack in its __init__, and then passes them to the
        base class __init__
        """

        self.lexer = lexer
        self.yacc = yacc
        self.error_stack = error_stack

    def parse(self, input_str):
        """
        Parse input_str, returning a tuple
            (error_stack, ast)
        representing the status of the parse, and the associated AST

        status - a list of strings representing the errors detected in parsing,
            stacked in order of generation.
        parse_tree - a ValueTree representing the abstract syntax tree (AST)
            resulting from the parse.

        The status of the parse is:
            [] - meaning that no problems were encountered, and parse_tree
                is complete
            non empty [] - meaning that some kind of problems were encountered 
                and status contains a list of diagnostic strings.
                
        """

        # Get rid of old error messages
        self.error_stack.clear()

        # now parse.
        ast = self.yacc.parse(input_str, lexer=self.lexer)
        return (self.error_stack, ast)

    def unparse(self, ast):
        """
        Convert the ast back into a string, which when re-parsed
        results in the same parse tree.  The result need not be, and in
        general will not be, the same string as the original input.

        In general it hard to unparse in the absence of knowledge of the
        original grammar, so the derived class has to implement this, if
        at all.

        Unparsing is one way to save the result of a parse for later
        re-generation.  Saving the parse tree as a value shape is another.
        """

        raise ValueError(
            "No unparse method provided for {}".format(type(self)))
