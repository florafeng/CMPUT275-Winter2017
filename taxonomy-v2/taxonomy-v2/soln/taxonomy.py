from structviz import StructViz
from valuetree import ValueTree

viz_filename = "taxo-tree"
viz_format = [ '.png' ]

def get_yes_no(question):
    """
    Return a yes (True) or no (False) answer to the supplied question.
    """
    while True:
        print(question + " [y|n]")
        answer = input()
        answer = answer.strip().lower()
        if  len(answer) > 0:
            if answer[0] == 'y':
                return True
            if answer[0] == 'n':
                return False

        print("Please answer yes or no ...");

def get_nonblank_str(question):
    """
    Return a non-blank answer to the supplied question.
    """
    while True:
        print(question)
        answer = input()
        answer = answer.strip()
        if  len(answer) > 0:
            return answer

        print("Please provide a non-blank answer ...");

def identify_thing(tree):
    """
    This function takes a taxonomy tree and attempts to identify
    a thing by asking a series of questions.  If the thing can
    be identified, it provides the name of the thing.  If the thing
    cannot be identified, then it asks for the name of the thing,
    and a distinguishing question.  In the latter case, tree is
    modified to contain the new information.

    A taxonomy tree T is a instance of a ValueTree that represents a
    decision tree structured as follows.

    Internal nodes are questions.
    The value of each internal node of the tree corresponds to a
    discrimination question, that determines a characteristic, such as
    "Does it have 4 legs?" Each internal node has two children. Child 0
    is the decision tree to follow for a 'yes' answer, and child 1 is the
    decision tree to follow for a 'no' answer.

    Leaf nodes identify things.
    The value of each leaf node of the tree is a thing, which has been
    identified by following the decision path in the tree to this leaf.
    It may not in fact be the thing that the user is trying to identify.
    In which case one can update the tree with additional decision information.

    """

    children = tree.get_children()

    if (len(children) == 0):
        name = tree.get_value()
        question = "Is it a {}?" .format(name)

        yes_answer = get_yes_no(question)
        if yes_answer:
            print("{} Identified!" .format(name))
        else:
            print("I don't know what it is.")
            new_name = get_nonblank_str("What is it?")

            new_question = get_nonblank_str(
                "Give me a question where yes means a '{}'" \
                " and no means a '{}'"
                .format(new_name, name))

            # Replace the I vertex with a D and two I's
            yes_child = ValueTree(new_name)
            no_child = ValueTree(name)
            tree.set_value(new_question)
            tree.set_children([yes_child, no_child])
            # children[0].set_value = new_name
            # children[1].set_value = name

    elif (len(children) == 2):
        question = tree.get_value()
        yes_answer = get_yes_no(question)
        if yes_answer:
            identify_thing(children[0])
        else:
            identify_thing(children[1])

def find_paths_to_thing(tree, name):
    """
    Find the question/answer paths from the root of the taxonomy tree
    to the leaves that contain a thing with the given name.
    A name may occur multiple times in tree, so this returns all the
    paths.

    Each path looks like this:
    [ [ quest, answer ], [ quest, answer ], ... , [ quest, answer ] ]

    where quest is the discrimination question being asked, and answer
    is 'y' or 'n' depending on what answer is required of the question.

    Returns a list of paths.  If name does not occur in the taxonomy tree
    then the empty list is returned.

    """

    # THIS NEEDS TO BE RE-IMPLEMENTED USING ValueTree
    children = tree.get_children()
    if len(children) == 0:
        if tree.get_value() == name:
            return [ [ ] ]
        else:
            return []

    else:
        # accumulate yes and no paths
        yes_paths = find_paths_to_thing(children[0], name)
        no_paths = find_paths_to_thing(children[1], name)

        question = tree.get_value()
        # prefix answer and question to each path
        py = list( map(lambda e: [ [ question, 'y' ]] + e, yes_paths ) )
        pn = list( map(lambda e: [ [ question, 'n' ]] + e, no_paths ) )
        return py + pn


def do_things(tree):
    result = list()
    def get_things(tree):
        """
        Get things in tree

        Inputs:
            tree - taxonomy tree

        Outputs
            things - a list of alll the thing names in tree.  The
                list is unordered and may have duplicates.
        """
        # THIS NEEDS TO BE RE-IMPLEMENTED USING ValueTree

        children = tree.get_children()

        if (len(children) == 0):
            result.append(tree.get_value())

        elif (len(children) == 2):
            get_things(children[0])
            get_things(children[1])

        return result

    # Get the things and remove duplicates
    things_list = get_things(tree)
    things_list = sorted(set(things_list))
    print(" ".join(things_list))


def do_describe(tree):
    """
    Run the description dialog, where the user enters a thing name, and
    its description is extracted from the taxonomy table as a sequence of
    questions and answers.
    """

    while get_yes_no("Continue description?"):
        thing_name = get_nonblank_str(
            "What thing do you want to describe?")

        paths = find_paths_to_thing(tree, thing_name)

        if len(paths) == 0:
            print("There is no {} in the tree." .format(thing_name))
        elif len(paths) == 1:
            print("The unique instance of {} is determined by:"
                .format(thing_name) )
            for i in paths[0]:
                print(i)
        else:
            print("There are {} instances of {} determined by:"
                .format(len(paths), thing_name))
            case_num = 1;
            for p in paths:
                print( "Case {}:".format(case_num))
                for i in p:
                    print(i)
                case_num += 1

def do_identify(tree, do_structviz=False):
    """
    Perform the interactive thing identification.
    do_structviz=True means to output the potentially updated
    taxonomy tree.
    """
    while get_yes_no("Continue identification?"):
        print("Identify your thing")
        identify_thing(tree)
        if do_structviz:
            StructViz.update_viz(tree, viz_filename,
                style='compact', pause=0, format=viz_format)


def _test():
    e_structviz = True
    import doctest
    doctest.testmod()

def main():
    import argparse
    parser = argparse.ArgumentParser(
        description='Taxonomy service.',
        formatter_class=argparse.RawTextHelpFormatter,
        )

    parser.add_argument("-s",
        help="Name of startup taxonomy database.",
        nargs="?",
        type=str,
        dest="taxo_startup_file",
        )

    parser.add_argument("-u",
        help="Name of updated taxonomy database.",
        nargs="?",
        type=str,
        dest="taxo_update_file",
        )

    parser.add_argument("--things",
        help="Display ordered list of things in the taxonomy.",
        action="store_true",
        dest="do_things")

    parser.add_argument("--describe",
        help="Enter describe mode that gives questions\nand answers that classify a given thing.",
        action="store_true",
        dest="do_describe")

    parser.add_argument("--doctest",
        help="Run doctests instead.",
        action="store_true",
        dest="do_doctest")

    parser.add_argument("--viz",
        help="Enable data structure visualization.",
        action="store_true",
        dest="do_structviz")

    args = parser.parse_args()

    # To run doctest instead of normal interactive service
    global enable_structviz
    if args.do_doctest:
        print("Running doctests")
        enable_structviz = False
        _test()
        exit()

    # Read in the taxonomy tree
    if args.taxo_startup_file:
        f = open(args.taxo_startup_file, "r", encoding="utf-8")
        # DANGER DANGER eval of external string
        valshape = eval(f.read())
        tree = ValueTree.valshape_to_tree(valshape)
        f.close
    else:
        # A default testing tree
        valshape = ('Does it have 4 legs?', [
            ('Can you ride it?', [ ('horse', []), ('dog', []) ], ),
            ('Does it have hands?', [ ('monkey', []), ('bird', []) ] )
            ])

        # Another testing tree with two instances of horse.
        valshape = ('Does it have 4 legs?', [
            ('Can you ride it?', [ ('horse', []),
                ('Was it a puppy?', [ ('dog', []), ('horse', []) ] ) ] ),
            ('Does it have hands?', [ ('monkey', []), ('bird', []) ] )
            ])

        tree = ValueTree.valshape_to_tree(valshape)

    # For visualization

    if args.do_structviz:
        StructViz.update_viz(tree, viz_filename,
            style='compact', pause=0, format=viz_format)

    if args.do_things:
        do_things(tree)

    elif args.do_describe:
        do_describe(tree)

    else:
        do_identify(tree, args.do_structviz)

    # Dump out the updated tree if requested
    if args.taxo_update_file:
        f = open(args.taxo_update_file, "w", encoding="utf-8")
        f.write(str(tree.tree_to_valshape()))
        f.write("\n")
        f.close

if __name__ == "__main__":
    main()
