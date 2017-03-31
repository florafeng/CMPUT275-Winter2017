from valuetree import ValueTree

def _test():
    e_structviz = True
    import doctest
    doctest.testmod()

def convert_tree(old):
    if old[0] == 'D':
        return ValueTree(old[1], 
            [ convert_tree(old[2]), convert_tree(old[3]) ])

    return ValueTree(old[1])

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

    parser.add_argument("--doctest",
        help="Run doctests instead.",
        action="store_true",
        dest="do_doctest")

    args = parser.parse_args()

    # To run doctest instead of normal interactive service
    global enable_structviz
    if args.do_doctest:
        print("Running doctests")
        _test()
        exit()

    # Read in the taxonomy tree
    if args.taxo_startup_file:
        f = open(args.taxo_startup_file, "r", encoding="utf-8")
        # DANGER DANGER eval of external string
        tree = eval(f.read())
        f.close

    # Dump out the updated tree if requested
    if args.taxo_update_file:
        f = open(args.taxo_update_file, "w", encoding="utf-8")

        valshape = convert_tree(tree).tree_to_valshape()
        f.write(str(valshape))
        f.write("\n")
        f.close

        # verify
        print("converted tree:", valshape)
        t_test = ValueTree.valshape_to_tree(valshape)

if __name__ == "__main__":
    main()
