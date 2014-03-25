# PyCalc

## Description

PyCalc is a CLI RPN calculator written in python with its own stack-based programming language that enables to easily extend its functionality.

To initiate it:

    $ ./main.py
    
## Simple examples

Press ENTER key to execute the command.

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

## List of operators  

### Math

Command | Inputs | Outputs | Description
--- | --- | --- | ---
**+** | 2 | 1 | Sum of two numbers. Aplied over two strings, it catenates them
**-** | 2 | 1 | Difference of two numbers
**\*** | 2 | 1 | Multiplication of two numbers
**/** | 2 | 1 | Division of two numbers
**pow** | 2 | 1 | Power of two numbers
**exp** | 1 | 1 | Power of e to the number passed as input
**sin** | 1 | 1 | Sine of the number passed as input
**cos** | 1 | 1 | Cosine of the number passed as input
**tan** | 1 | 1 | Tangent of the number passed as input
**neg** | 1 | 1 | Negative of the number passed as input
**inv** | 1 | 1 | Inverse of the number passed as input

### Stack

Command | Inputs | Outputs | Description
--- | --- | --- | ---
**dup** | 1 | 2 | Duplicate the top element of the stack
**drop** | 1 | 0 | Delete the top element of the stack
**cls** | - | 0 | Clears the stack completely
**[** | - | 0 | Begins a list. All the commands after this will be stored in the list
**]** | - | 1 | Ends a list and puts it in the stack

### Other

Command | Inputs | Outputs | Description
--- | --- | --- | ---
**vars** | 0 | 1 | Returns a list of all defined variables
**ret** | 0 | - | Returns from a function
**print** | 1 | 0 | Deletes and prints the top element of the stack.


