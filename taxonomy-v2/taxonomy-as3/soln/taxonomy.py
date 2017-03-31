from structviz import StructViz

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

    A taxonomy tree T is a decision tree structured as follows.

    Each internal vertex (or node) of the tree corresponds to a 
    discrimination question, that determines a characteristic,
    such as "Does it have 4 legs?"

    It has this structure:
      [ "D", question, T_yes, T_no ]
    where question is a string that poses a question and expects a
    Yes or No answer.  Depending on the answer, the decision path
    navigates down the yes or no decision sub tree.

    Each leaf node of the tree is an identification question, 
    which confirms that a particular object with the given name has 
    been identified.

    It has the structure:
      [ "I", name ]
    """

    node_type = tree[0]
    if node_type == "D":
        (question, yes_tree, no_tree) = tree[1:]
        yes_answer = get_yes_no(question)
        if yes_answer:
            identify_thing(yes_tree)
        else:
            identify_thing(no_tree)

    elif node_type == "I":
        name = tree[1]
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

            # Now at this point we need to update the tree to store the
            # new information.

            # Replace the I vertex with a D and two I's
            yes_tree = [ "I", new_name ]
            no_tree = [ "I", name ]
            tree[0] = "D"
            tree[1] = new_question
            tree.append(yes_tree)
            tree.append(no_tree)
    
def do_things(tree):
    def get_things(tree):
        """
        Get things in tree

        Inputs: 
            tree - taxonomy tree

        Outputs
            things - a list of alll the thing names in tree.  The
                list is unordered and may have duplicates.
        """
        if tree[0] == 'I':
            return [ tree[1] ]
        else:
            return get_things(tree[2]) + get_things(tree[3])

    # Get the things and remove duplicates
    things_list = get_things(tree)
    things_list = sorted(set(things_list))
    print(" ".join(things_list))

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
    if tree[0] == 'I':
        if tree[1] == name:
            return [ [ ] ]
        else:
            return [ ]

    else:
        # accumulate yes and no paths
        yes_tree = tree[2]
        no_tree = tree[3]
        yes_paths = find_paths_to_thing(yes_tree, name)
        no_paths = find_paths_to_thing(no_tree, name)

        question = tree[1]
        # prefix answer and question to each path
        py = list( map(lambda e: [ [ question, 'y' ]] + e, yes_paths ) )
        pn = list( map(lambda e: [ [ question, 'n' ]] + e, no_paths ) )
        return py + pn

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
        tree = eval(f.read())
        f.close
    else:
        # A default testing tree
        tree = ['D', 'Does it have 4 legs?', 
            ['D', 'Can you ride it?', ['I', 'horse'], ['I', 'dog']], 
            ['D', 'Does it have hands?', ['I', 'monkey'], ['I', 'bird']]]

        # Another testing tree with two instances of horse.
        tree = ['D', 'Does it have 4 legs?', 
            ['D', 'Can you ride it?', ['I', 'horse'], 
                ['D', 'Was it a puppy?', ['I', 'dog'], ['I', 'horse']]], 
            ['D', 'Does it have hands?', ['I', 'monkey'], ['I', 'bird']]]

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
        f.write(str(tree))
        f.write("\n")
        f.close

if __name__ == "__main__":
    main()
