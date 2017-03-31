import sys

"""
Morning problem

Your task has two parts:

1 - implement a new class method called parse() that encapsulates all
the ad-hoc code in bad_calc.py for parsing strings representing into
corresponding ExprTree objects. You will need to do this first.

2 - implement a new instance method of ExprTree called unparse() that
takes the expression tree and unparses it into a string that is an
equivalent fully parenthesized formula.

If you run this:
    python3 good_calc.py < tests.txt

Where tests.txt is this sample input:
(42)
1
1 + 2
(1 + 3) * (4 + 5)
1 + 2 + 3 + 4 + 5
((((1 + 2) + 3) + 4) + 5)
(1 + (2 + (3 + (4 + 5))))
(1 + 2) * (3 * (4 + 5)) * 6 + 7
-1
1 - 2
- - - 1
1 -- 2

you should get this expected output:

Unparse: 42
Result: 42
Unparse: 1
Result: 1
Unparse: (1 + 2)
Result: 3
Unparse: ((1 + 3) * (4 + 5))
Result: 36
Unparse: ((((1 + 2) + 3) + 4) + 5)
Result: 15
Unparse: ((((1 + 2) + 3) + 4) + 5)
Result: 15
Unparse: (1 + (2 + (3 + (4 + 5))))
Result: 15
Unparse: ((((1 + 2) * (3 * (4 + 5))) * 6) + 7)
Result: 493
Unparse: (- 1)
Result: -1
Unparse: (1 - 2)
Result: -1
Unparse: (- (- (- 1)))
Result: -1
Unparse: (1 - (- 2))
Result: 3
Done

"""



from structviz import StructViz
from exprtree import *

# Ask for an expression until get EOF or blank line
for s in sys.stdin:
    s = s.strip()
    if s == "": 
        break

    # Attempt to parse it into an ExprTree
    try:
        t = ExprTree.parse(s)
    except ValueError as e:
        print("Bad conversion: {}".format(e))
        # back for another expression
        continue

    # unparse
    print("Unparse:", t.unparse())

    # For visualization
    if False:
        file_name = "t"
        print("Resulting ExprTree in '{}.dot' and '{}.dot.png'".
            format(file_name, file_name))
        disp = { 'op_to_fn' : ExprTree.op_to_fn, 'expr' : t }

        StructViz.update_viz(disp, file_name, 
            style='compact', pause=0, format=['png'])

    # Attempt to evaluate
    try:
        r = t.evaluate()
        print("Result: {}".format(r))
    except Exception as e:
        print("Evaluation error: {}".format(e))

    # Back for more

print("Done")
