Weekly Exercise 4

The goal of this exercise is to give you more OOP practice, and to
introduce you to the code generation aspect of compiling a language. We
started with the simple calculator that we used this week as a study in
how to read OO programs. In the calculator, we took the AST (abstract
syntax tree) from the compiler and evaluated it to produce a numerical
result (with side effects of setting variables to values in the
expression).

In this exercise, you will instead walk over the AST and produce Python
code, that when executed performs the same calculations.

The code you want to work (and submit) is in compiler.py, and optimizer.py

Detailed descriptions of the task are in these two files.

To help you visualize the AST, the AST for this expression

x = (y+1) + 2 * (x * - - 3) + sqr(2)

is in: ast-opt.dot  ast-opt.pdf  ast-opt.png

Main Task:

The module compiler.py contains class definition for Compiler.  The main 
code generator is a method called 'compile'. You should NOT be changing 
this method. Most of the work is done in the method called 'compile_ast'. 
This is where most of your changes should be made.  In particular you need
to implement the handling of 'set' and 'apply' nodes in the AST.

Implementation strategy:  first get code generation working for expressions
that do not involve any variable assignment operations (e.g. x = 2).
Then worry about how to deal with assignment statements.

Bonus Task:

Bonus marks will be awarded for performing optimizations on the AST that
remove repeated negations (like replacing x * - - - - - y by x * -y)
prior to code generation.  These optimizations are done in the module
optimizer.py.  There is a dummy stub for the negation optimizer, along with
some hints of how it should work.

Note that you can do the bonus task even if the code generation task is not
complete.

Submission:

Submit a zip containing the two files: compiler.py and optimizer.py.
