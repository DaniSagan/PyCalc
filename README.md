# PyCalc

## Description

PyCalc is a CLI RPN calculator written in python with its own stack-based programming language that enables to easily extend its functionality.

To initiate it:

    $ ./main.py
    
## Simple examples

Press ENTER key for executing the command.

Sum of two numbers:

    >> 23 47 +
    -------------------
    70.0 : number
    -------------------

Difference of two numbers:

    >> 23 47 -
    -------------------
    -24.0 : number
    -------------------

Multiplication:

    >> 23 47 *
    -------------------
    1081.0 : number
    -------------------

Division:
    
    >> 23 47 /
    -------------------
    0.489361702128 : number
    -------------------
    
Combination of multiple operations (2+3*7)/((5+8)*4):

    >> 2 3 7 * + 5 8 + 4 * /
    -------------------
    0.442307692308 : number
    -------------------

Exiting the program:
    
    >> quit
    
