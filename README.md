# PyCalc

## Description

PyCalc is a CLI RPN calculator written in python with its own stack-based programming language that enables to easily extend its functionality.

To initiate it:

    $ ./main.py
    
## Simple examples

Press ENTER key to execute each command.

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

A slightly more complicated example. Create 2 complex numbers, multiply them, obtain the result's argument in radians and convert it to degrees:

    >> 2 2 complex
    -------------------
    2.0+2.0i : complex
    -------------------
    >> 1 2 complex  
    -------------------
    2.0+2.0i : complex
    1.0+2.0i : complex
    -------------------
    >> *
    -------------------
    -2.0+6.0i : complex
    -------------------
    >> arg
    -------------------
    1.89254688119 : number
    -------------------
    >> 180 * pi /
    -------------------
    108.434948823 : number
    -------------------

Or in one line:
    
    >> 2 2 complex 1 2 complex * arg 180 * pi /
    -------------------
    108.434948823 : number
    -------------------

A text string:

    >> "Hello World!"
    -------------------
    "Hello World!" : string
    -------------------    

To exit the program:
    
    >> quit

For more information please visit the [wiki](https://github.com/DaniSagan/PyCalc/wiki)
