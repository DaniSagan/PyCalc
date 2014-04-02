#! /usr/bin/python
# -*- coding=utf-8 -*-

import math
import dfv.data
from main import App
import os
import copy

class Operator:
    def __init__(self):
        self.type = "none"
        self.category = "operator"
        self.word = "none"
        
    def execute(self, stack, variables):
        pass
    
    def __str__(self):
        return self.word     
    
        
class Sum(Operator):
    def __init__(self):
        Operator.__init__(self)
        self.type = "sum"
        self.word = "+"
        
    def execute(self, stack, variables):
        if len(stack) >= 2:            
            if stack[-1].type == "number" and stack[-2].type == "number":
                n2 = stack.pop()
                n1 = stack.pop()
                stack.append(dfv.data.Number(n1.value + n2.value))
            elif stack[-1].type == "integer" and stack[-2].type == "integer":
                n2 = stack.pop()
                n1 = stack.pop()
                stack.append(dfv.data.Integer(n1.value + n2.value))
            elif stack[-1].type == "complex" and stack[-2].type == "complex":
                n2 = stack.pop()
                n1 = stack.pop()
                stack.append(dfv.data.Complex(n1.real_value + n2.real_value, n1.imag_value + n2.imag_value))
            elif stack[-1].type == "string" and stack[-2].type == "string":
                n2 = stack.pop()
                n1 = stack.pop()
                stack.append(dfv.data.String(n1.value + n2.value))
            elif stack[-1].type == "list" and stack[-2].type == "list":
                n2 = stack.pop()
                n1 = stack.pop()
                res = []
                res.extend(n1.values)
                res.extend(n2.values)
                stack.append(dfv.data.List(parent=n1.parent, values=res))
            else:
                stack.append(dfv.data.Error("Types not supported"))
        else:
            stack.append(dfv.data.Error("Not enough parameters"))
            
      

            
class Diff(Operator):
    def __init__(self):
        Operator.__init__(self)
        self.type = "diff"
        self.word = "-"
        
    def execute(self, stack, variables):
        if len(stack) >= 2:            
            if stack[-1].type == "number" and stack[-2].type == "number":
                n2 = stack.pop()
                n1 = stack.pop()
                stack.append(dfv.data.Number(n1.value - n2.value))
            elif stack[-1].type == "integer" and stack[-2].type == "integer":
                n2 = stack.pop()
                n1 = stack.pop()
                stack.append(dfv.data.Integer(n1.value - n2.value))
            elif stack[-1].type == "complex" and stack[-2].type == "complex":
                n2 = stack.pop()
                n1 = stack.pop()
                stack.append(dfv.data.Complex(n1.real_value - n2.real_value, n1.imag_value - n2.imag_value))
            else:
                stack.append(dfv.data.Error("Types not supported"))
        else:
            stack.append(dfv.data.Error("Not enough parameters")) 
            

class Mult(Operator):
    def __init__(self):
        Operator.__init__(self)
        self.type = "mult"
        self.word = "*"
        
    def execute(self, stack, variables):
        if len(stack) >= 2:            
            if stack[-1].type == "number" and stack[-2].type == "number":
                n2 = stack.pop()
                n1 = stack.pop()
                stack.append(dfv.data.Number(n1.value * n2.value))
            elif stack[-1].type == "integer" and stack[-2].type == "integer":
                n2 = stack.pop()
                n1 = stack.pop()
                stack.append(dfv.data.Integer(n1.value * n2.value))
            elif stack[-1].type == "complex" and stack[-2].type == "complex":
                n2 = stack.pop()
                n1 = stack.pop()
                stack.append(dfv.data.Complex(n1.real_value*n2.real_value - n1.imag_value*n2.imag_value, 
                                          n1.real_value*n2.imag_value + n1.imag_value*n2.real_value))
            elif stack[-1].type == "number" and stack[-2].type == "list":
                n2 = stack.pop()
                n1 = stack.pop()
                res = []
                #print int(n2.value)
                for k in range(int(n2.value)):
                    res.extend(n1.values)
                stack.append(dfv.data.List(parent=n1.parent, values=res))
            else:
                stack.append(dfv.data.Error("Types not supported"))
        else:
            stack.append(dfv.data.Error("Not enough parameters")) 
            
            
class Pow(Operator):
    def __init__(self):
        Operator.__init__(self)
        self.type = "pow"
        self.word = "**"
        
    def execute(self, stack, variables):
        if len(stack) >= 2:            
            if stack[-1].type == "number" and stack[-2].type == "number":
                n2 = stack.pop()
                n1 = stack.pop()
                stack.append(dfv.data.Number(n1.value ** n2.value))
            elif stack[-1].type == "integer" and stack[-2].type == "integer":
                n2 = stack.pop()
                n1 = stack.pop()
                stack.append(dfv.data.Integer(n1.value ** n2.value))
            else:
                stack.append(dfv.data.Error("Types not supported"))
        else:
            stack.append(dfv.data.Error("Not enough parameters")) 
            
  
class Div(Operator):
    def __init__(self):
        Operator.__init__(self)
        self.type = "div"
        self.word = "/"
        
    def execute(self, stack, variables):
        if len(stack) >= 2:            
            if stack[-1].type == "number" and stack[-2].type == "number":
                if stack[-1].value == 0:
                    stack.append(dfv.data.Error("Cannot divide by 0"))
                else:
                    n2 = stack.pop()
                    n1 = stack.pop()
                    stack.append(dfv.data.Number(n1.value / n2.value))
            elif stack[-1].type == "integer" and stack[-2].type == "integer":
                if stack[-1].value == 0:
                    stack.append(dfv.data.Error("Cannot divide by 0"))
                else:
                    n2 = stack.pop()
                    n1 = stack.pop()
                    stack.append(dfv.data.Integer(int(n1.value / n2.value)))
            elif stack[-1].type == "complex" and stack[-2].type == "complex":
                if stack[-1].real_value == 0 and stack[-1].imag_value == 0:
                    stack.append(dfv.data.Error("Cannot divide by 0"))
                else:
                    n2 = stack.pop()
                    n1 = stack.pop()
                    a = n1.real_value
                    b = n1.imag_value
                    c = n2.real_value
                    d = n2.imag_value
                    stack.append(dfv.data.Complex((a*c+b*d)/(c**2+d**2), 
                                                  (b*c-a*d)/(c**2+d**2)))
            else:
                stack.append(dfv.data.Error("Types not supported"))
        else:
            stack.append(dfv.data.Error("Not enough parameters"))
            
            
class ToComplex(Operator):
    def __init__(self):
        Operator.__init__(self)
        self.type = "complex"
        self.word = "complex"
        
    def execute(self, stack, variables):
        if len(stack) >= 2:            
            if stack[-1].type == "number" and stack[-2].type == "number":
                n2 = stack.pop()
                n1 = stack.pop()
                stack.append(dfv.data.Complex(n1.value, n2.value))
            else:
                stack.append(dfv.data.Error("Types not supported"))
        else:
            stack.append(dfv.data.Error("Not enough parameters"))

            
class Exp(Operator):
    def __init__(self):
        Operator.__init__(self)
        self.type = "exp"
        self.word = "exp"
        
    def execute(self, stack, variables):
        if len(stack) >= 1:            
            if stack[-1].type == "number":
                n1 = stack.pop()
                stack.append(dfv.data.Number(math.exp(n1.value)))
            elif stack[-1].type == "complex":
                n1 = stack.pop()
                stack.append(dfv.data.Complex(math.exp(n1.real_value)*math.cos(n1.imag_value),
                                              math.exp(n1.real_value)*math.sin(n1.imag_value)))
            else:
                stack.append(dfv.data.Error("Types not supported"))
        else:
            stack.append(dfv.data.Error("Not enough parameters"))


class Abs(Operator):
    def __init__(self):
        Operator.__init__(self)
        self.type = "abs"
        self.word = "abs"
        
    def execute(self, stack, variables):
        if len(stack) >= 1:            
            if stack[-1].type == "number":
                n1 = stack.pop()
                stack.append(dfv.data.Number(abs(n1.value)))
            elif stack[-1].type == "integer":
                n1 = stack.pop()
                stack.append(dfv.data.Integer(abs(n1.value)))
            elif stack[-1].type == "complex":
                n1 = stack.pop()
                stack.append(dfv.data.Number(math.sqrt(n1.real_value**2 + n1.imag_value**2)))
            elif stack[-1].type == "list":
                n1 = stack.pop()
                stack.append(dfv.data.Integer(len(n1.values)))
            else:
                stack.append(dfv.data.Error("Types not supported"))
        else:
            stack.append(dfv.data.Error("Not enough parameters"))
            
            
class Arg(Operator):
    def __init__(self):
        Operator.__init__(self)
        self.type = "arg"
        self.word = "arg"
        
    def execute(self, stack, variables):
        if len(stack) >= 1:            
            if stack[-1].type == "number":
                n1 = stack.pop()
                stack.append(dfv.data.Number(0))
            if stack[-1].type == "complex":
                n1 = stack.pop()
                stack.append(dfv.data.Number(math.atan2(n1.imag_value, n1.real_value)))
            else:
                stack.append(dfv.data.Error("Types not supported"))
        else:
            stack.append(dfv.data.Error("Not enough parameters"))


class Sin(Operator):
    def __init__(self):
        Operator.__init__(self)
        self.type = "sin"
        self.word = "sin"
        
    def execute(self, stack, variables):
        if len(stack) >= 1:            
            if stack[-1].type == "number":
                n1 = stack.pop()
                stack.append(dfv.data.Number(math.sin(n1.value)))
            else:
                stack.append(dfv.data.Error("Types not supported"))
        else:
            stack.append(dfv.data.Error("Not enough parameters"))


class Asin(Operator):
    def __init__(self):
        Operator.__init__(self)
        self.type = "asin"
        self.word = "asin"
        
    def execute(self, stack, variables):
        if len(stack) >= 1:            
            if stack[-1].type == "number":
                n1 = stack.pop()
                stack.append(dfv.data.Number(math.asin(n1.value)))
            else:
                stack.append(dfv.data.Error("Types not supported"))
        else:
            stack.append(dfv.data.Error("Not enough parameters"))


class Cos(Operator):
    def __init__(self):
        Operator.__init__(self)
        self.type = "cos"
        self.word = "cos"
        
    def execute(self, stack, variables):
        if len(stack) >= 1:            
            if stack[-1].type == "number":
                n1 = stack.pop()
                stack.append(dfv.data.Number(math.cos(n1.value)))
            else:
                stack.append(dfv.data.Error("Types not supported"))
        else:
            stack.append(dfv.data.Error("Not enough parameters"))


class Acos(Operator):
    def __init__(self):
        Operator.__init__(self)
        self.type = "acos"
        self.word = "acos"
        
    def execute(self, stack, variables):
        if len(stack) >= 1:            
            if stack[-1].type == "number":
                n1 = stack.pop()
                stack.append(dfv.data.Number(math.acos(n1.value)))
            else:
                stack.append(dfv.data.Error("Types not supported"))
        else:
            stack.append(dfv.data.Error("Not enough parameters"))


class Tan(Operator):
    def __init__(self):
        Operator.__init__(self)
        self.type = "tan"
        self.word = "tan"
        
    def execute(self, stack, variables):
        if len(stack) >= 1:            
            if stack[-1].type == "number":
                n1 = stack.pop()
                stack.append(dfv.data.Number(math.tan(n1.value)))
            else:
                stack.append(dfv.data.Error("Types not supported"))
        else:
            stack.append(dfv.data.Error("Not enough parameters"))
            
            
class Atan(Operator):
    def __init__(self):
        Operator.__init__(self)
        self.type = "atan"
        self.word = "atan"
        
    def execute(self, stack, variables):
        if len(stack) >= 1:            
            if stack[-1].type == "number":
                n1 = stack.pop()
                stack.append(dfv.data.Number(math.atan(n1.value)))
            else:
                stack.append(dfv.data.Error("Types not supported"))
        else:
            stack.append(dfv.data.Error("Not enough parameters"))
            
            
class Atan2(Operator):
    def __init__(self):
        Operator.__init__(self)
        self.type = "atan2"
        self.word = "atan2"
        
    def execute(self, stack, variables):
        if len(stack) >= 2:            
            if stack[-2].type == "number" and stack[-1].type == "number":
                n2 = stack.pop()
                n1 = stack.pop()
                stack.append(dfv.data.Number(math.atan2(n1.value, n2.value)))
            else:
                stack.append(dfv.data.Error("Types not supported"))
        else:
            stack.append(dfv.data.Error("Not enough parameters"))


class Ln(Operator):
    def __init__(self):
        Operator.__init__(self)
        self.type = "ln"
        self.word = "ln"
        
    def execute(self, stack, variables):
        if len(stack) >= 1:            
            if stack[-1].type == "number":
                n1 = stack.pop()
                stack.append(dfv.data.Number(math.log(n1.value)))
            elif stack[-1].type == "complex":
                n1 = stack.pop()
                r = math.sqrt(n1.real_value**2 + n1.imag_value)
                a = math.atan2(n1.imag_value, n1.real_value)
                stack.append(dfv.data.Complex(math.log(r), a))
            else:
                stack.append(dfv.data.Error("Types not supported"))
        else:
            stack.append(dfv.data.Error("Not enough parameters"))

            
class Neg(Operator):
    def __init__(self):
        Operator.__init__(self)
        self.type = "neg"
        self.word = "neg"
        
    def execute(self, stack, variables):
        if len(stack) >= 1:            
            if stack[-1].type == "number":
                n1 = stack.pop()
                stack.append(dfv.data.Number(-n1.value))
            elif stack[-1].type == "integer":
                n1 = stack.pop()
                stack.append(dfv.data.Integer(-n1.value))
            elif stack[-1].type == "bool":
                n1 = stack.pop()
                stack.append(dfv.data.Bool(not n1.value))
            else:
                stack.append(dfv.data.Error("Types not supported"))
        else:
            stack.append(dfv.data.Error("Not enough parameters"))  
            
class Inv(Operator):
    def __init__(self):
        Operator.__init__(self)
        self.type = "inv"
        self.word = "inv"
        
    def execute(self, stack, variables):
        if len(stack) >= 1:            
            if stack[-1].type == "number":
                if stack[-1].value == 0:
                    stack.append(dfv.data.Error("Cannot divide by 0"))
                else:
                    n1 = stack.pop()
                    stack.append(dfv.data.Number(1.0/n1.value))
            else:
                stack.append(dfv.data.Error("Types not supported"))
        else:
            stack.append(dfv.data.Error("Not enough parameters"))     


class Drop(Operator):
    def __init__(self):
        Operator.__init__(self)
        self.type = "drop"
        self.word = "drop"
        
    def execute(self, stack, variables):
        if len(stack) >= 1:
            stack.pop()
        else:
            stack.append(dfv.data.Error("Not enough parameters")) 
            
            
class Dup(Operator):
    def __init__(self):
        Operator.__init__(self)
        self.type = "dup"
        self.word = "dup"
        
    def execute(self, stack, variables):
        if len(stack) >= 1:
            stack.append(copy.deepcopy(stack[-1]))
        else:
            stack.append(dfv.data.Error("Not enough parameters"))
            
            
class Def(Operator):
    def __init__(self):
        Operator.__init__(self)
        self.type = "def"
        self.word = "def"
        
    def execute(self, stack, variables):
        if len(stack) >= 2:            
            if stack[-1].type == "list":
                n1 = stack.pop()
                for n in reversed(n1):
                    stack.append(n)
                    self.execute(stack, variables)
            elif stack[-1].type == "string" and stack[-2].type == "string":
                n2 = stack.pop()
                n1 = stack.pop()
                if n2.value.startswith(".") and variables["curr_function"] != None: 
                    variables["curr_function"].locals[n2.value] = n1
                else: 
                    variables[n2.value] = n1
            elif stack[-1].type == "string" and stack[-2].type in ["number", "integer"]:
                #if stack[-1].value not in variables:
                n2 = stack.pop()
                n1 = stack.pop()
                if n2.value.startswith(".") and variables["curr_function"] != None: 
                    variables["curr_function"].locals[n2.value] = n1
                else: 
                    variables[n2.value] = n1
            elif stack[-1].type == "string" and stack[-2].type == "bool":
                #if stack[-1].value not in variables:
                n2 = stack.pop()
                n1 = stack.pop()
                if n2.value.startswith(".") and variables["curr_function"] != None: 
                    variables["curr_function"].locals[n2.value] = n1
                else: 
                    variables[n2.value] = n1
            elif stack[-1].type == "string" and stack[-2].type == "complex":
                n2 = stack.pop()
                n1 = stack.pop()
                if n2.value.startswith(".") and variables["curr_function"] != None: 
                    variables["curr_function"].locals[n2.value] = n1
                else: 
                    variables[n2.value] = n1
            elif stack[-1].type == "string" and stack[-2].type == "list":
                n2 = stack.pop()
                n1 = stack.pop()
                if n2.value.startswith(".") and variables["curr_function"] != None: 
                    variables["curr_function"].locals[n2.value] = n1
                else: 
                    variables[n2.value] = n1
            elif stack[-1].type == "string":
                n2 = stack.pop()
                n1 = stack.pop()
                if n2.value.startswith(".") and variables["curr_function"] != None: 
                    variables["curr_function"].locals[n2.value] = n1
                else: 
                    variables[n2.value] = n1
            else:
                stack.append(dfv.data.Error("Types not supported"))
        else:
            stack.append(dfv.data.Error("Not enough parameters"))
            
            
class Cls(Operator):
    def __init__(self):
        Operator.__init__(self)
        self.type = "cls"
        self.word = "cls"
        
    def execute(self, stack, variables):
        stack.values[:] = []
        
class Eval(Operator):
    def __init__(self):
        Operator.__init__(self)
        self.type = "eval"
        self.word = "."
        
    def execute(self, stack, variables):
        pass
        
class StartList(Operator):
    def __init__(self):
        Operator.__init__(self)
        self.type = "start_list"
        self.word = "["
        
    def execute(self, stack, variables):
        if variables["curr_list"] == None:
            stack.append(dfv.data.List(parent=None))
            variables["curr_list"] = stack[-1]
        else:
            variables["curr_list"].append(dfv.data.List(parent=variables["curr_list"]))
            variables["curr_list"] = variables["curr_list"][-1]
            
class EndList(Operator):
    def __init__(self):
        Operator.__init__(self)
        self.type = "end_list"
        self.word = "]"
        
    def execute(self, stack, variables):
        if variables["curr_list"] == None:
            stack.append(dfv.data.Error("There is no list"))
        else:
            variables["curr_list"] = variables["curr_list"].parent
    
    
class Fun(Operator):
    def __init__(self):
        Operator.__init__(self)
        self.type = "fun"
        self.word = "fun"
        
    def execute(self, stack, variables):
        if len(stack) >= 2:            
            if stack[-1].type == "string" and stack[-2].type == "string":
                n2 = stack.pop()
                n1 = stack.pop()
                variables[n2.value] = dfv.data.Function([n1], name=n2.value)
            elif stack[-1].type == "string" and stack[-2].type in ["number", "integer"]:
                n2 = stack.pop()
                n1 = stack.pop()
                variables[n2.value] = dfv.data.Function([n1], name=n2.value)
            elif stack[-1].type == "string" and stack[-2].type == "complex":
                n2 = stack.pop()
                n1 = stack.pop()
                variables[n2.value] = dfv.data.Function([n1], name=n2.value)
            elif stack[-1].type == "string" and stack[-2].type == "list":
                n2 = stack.pop()
                n1 = stack.pop()
                variables[n2.value] = dfv.data.Function(n1.values, name=n2.value)
            else:
                stack.append(dfv.data.Error("Types not supported"))
        else:
            stack.append(dfv.data.Error("Not enough parameters"))   
            
            
class Cat(Operator):
    def __init__(self):
        Operator.__init__(self)
        self.type = "cat"
        self.word = "cat"
        
    def execute(self, stack, variables):
        if len(stack) >= 2:
            if stack[-1].type == "string" and stack[-2].type == "string":
                n2 = stack.pop()
                n1 = stack.pop()
                stack.append(dfv.data.String(n1.value + n2.value))
            elif stack[-1].type == "list" and stack[-2].type == "list":
                n2 = stack.pop()
                n1 = stack.pop()
                n1.values.extend(n2.values)
                stack.append(dfv.data.List(parent=variables["curr_list"], values=n1.values))
            else:
                stack.append(dfv.data.Error("Types not supported"))
        else:
            stack.append(dfv.data.Error("Not enough parameters"))
     

class If(Operator):
    def __init__(self):
        Operator.__init__(self)
        self.type = "if"
        self.world = "if"
        
    def execute(self, stack, variables):
        if len(stack) >= 2:
            if stack[-1].type == "bool" and stack[-2].type == "list":
                n2 = stack.pop()
                n1 = stack.pop()
                if n2.value == True:
                    for cmd in n1.values:
                        cmd.execute(stack, variables)
            else:
                stack.append(dfv.data.Error("Types not supported"))
        else:
            stack.append(dfv.data.Error("Not enough parameters"))  
            
            
class IfElse(Operator):
    def __init__(self):
        Operator.__init__(self)
        self.type = "ifelse"
        self.world = "ifelse"
        
    def execute(self, stack, variables):
        if len(stack) >= 3:
            if stack[-1].type == "bool" and stack[-2].type == "list" and stack[-3].type == "list":
                n3 = stack.pop()
                n2 = stack.pop()
                n1 = stack.pop()
                if n3.value == True:
                    for cmd in n1.values:
                        cmd.execute(stack, variables)
                else:
                    for cmd in n2.values:
                        cmd.execute(stack, variables)
            else:
                stack.append(dfv.data.Error("Types not supported"))
        else:
            stack.append(dfv.data.Error("Not enough parameters")) 
            
            
class Not(Operator):
    def __init__(self):
        Operator.__init__(self)
        self.type = "not"
        self.world = "not"
        
    def execute(self, stack, variables):
        if len(stack) >= 1:
            if stack[-1].type == "bool":
                n1 = stack.pop()
                stack.append(dfv.data.Bool(not n1.value))
            else:
                stack.append(dfv.data.Error("Types not supported"))
        else:
            stack.append(dfv.data.Error("Not enough parameters"))  
            
            
class While(Operator):
    def __init__(self):
        Operator.__init__(self)
        self.type = "while"
        self.word = "while"
        
    def execute(self, stack, variables):
        if len(stack) >= 2:
            if stack[-1].type == "list" and stack[-2].type == "list":
                n2 = stack.pop()
                n1 = stack.pop()
                loop = True
                while loop:
                    for cmd in n2.values:
                        cmd.execute(stack, variables, variables["curr_function"])
                    res = stack.pop()
                    if res.type == "bool" and res.value == True:
                        for cmd in n1.values:
                            cmd.execute(stack, variables, variables["curr_function"])
                            if variables["ret_function"]: 
                                loop = False
                                break
                    else:
                        loop = False
            else:
                stack.append(dfv.data.Error("Types not supported"))
        else:
            stack.append(dfv.data.Error("Not enough parameters"))
            
            
class Eq(Operator):
    def __init__(self):
        Operator.__init__(self)
        self.type = "eq"
        self.word = "="
        
    def execute(self, stack, variables):
        if len(stack) >= 2:            
            if stack[-1].type == "bool" and stack[-2].type == "bool":
                n2 = stack.pop()
                n1 = stack.pop()
                stack.append(dfv.data.Bool(n1.value == n2.value))
            elif stack[-1].type == "number" and stack[-2].type == "number":
                n2 = stack.pop()
                n1 = stack.pop()
                stack.append(dfv.data.Bool(n1.value == n2.value))
            elif stack[-1].type == "integer" and stack[-2].type == "integer":
                n2 = stack.pop()
                n1 = stack.pop()
                stack.append(dfv.data.Bool(n1.value == n2.value))
            elif stack[-1].type == "complex" and stack[-2].type == "complex":
                n2 = stack.pop()
                n1 = stack.pop()
                stack.append(dfv.data.Bool(n1.real_value == n2.real_value and n1.imag_value == n2.imag_value))
            elif stack[-1].type == "string" and stack[-2].type == "string":
                n2 = stack.pop()
                n1 = stack.pop()
                stack.append(dfv.data.Bool(n1.value == n2.value))
            else:
                stack.append(dfv.data.Error("Types not supported"))
        else:
            stack.append(dfv.data.Error("Not enough parameters"))
            
            
class Neq(Operator):
    def __init__(self):
        Operator.__init__(self)
        self.type = "neq"
        self.word = "!="
        
    def execute(self, stack, variables):
        if len(stack) >= 2:            
            if stack[-1].type == "bool" and stack[-2].type == "bool":
                n2 = stack.pop()
                n1 = stack.pop()
                stack.append(dfv.data.Bool(n1.value != n2.value))
            elif stack[-1].type == "number" and stack[-2].type == "number":
                n2 = stack.pop()
                n1 = stack.pop()
                stack.append(dfv.data.Bool(n1.value != n2.value))
            elif stack[-1].type == "integer" and stack[-2].type == "integer":
                n2 = stack.pop()
                n1 = stack.pop()
                stack.append(dfv.data.Bool(n1.value != n2.value))
            elif stack[-1].type == "complex" and stack[-2].type == "complex":
                n2 = stack.pop()
                n1 = stack.pop()
                stack.append(dfv.data.Bool(n1.real_value != n2.real_value and n1.imag_value != n2.imag_value))
            elif stack[-1].type == "string" and stack[-2].type == "string":
                n2 = stack.pop()
                n1 = stack.pop()
                stack.append(dfv.data.Bool(n1.value == n2.value))
            else:
                stack.append(dfv.data.Error("Types not supported"))
        else:
            stack.append(dfv.data.Error("Not enough parameters"))     
            

class LessThan(Operator):
    def __init__(self):
        Operator.__init__(self)
        self.type = "less_than"
        self.word = "<"
        
    def execute(self, stack, variables):
        if len(stack) >= 2:            
            if stack[-1].type == "number" and stack[-2].type == "number":
                n2 = stack.pop()
                n1 = stack.pop()
                stack.append(dfv.data.Bool(n1.value < n2.value))
            elif stack[-1].type == "integer" and stack[-2].type == "integer":
                n2 = stack.pop()
                n1 = stack.pop()
                stack.append(dfv.data.Bool(n1.value < n2.value))
            elif stack[-1].type == "string" and stack[-2].type == "string":
                n2 = stack.pop()
                n1 = stack.pop()
                stack.append(dfv.data.Bool(n1.value < n2.value))
            else:
                stack.append(dfv.data.Error("Types not supported"))
        else:
            stack.append(dfv.data.Error("Not enough parameters"))

            
class LessEqThan(Operator):
    def __init__(self):
        Operator.__init__(self)
        self.type = "less_eq_than"
        self.word = "<="
        
    def execute(self, stack, variables):
        if len(stack) >= 2:            
            if stack[-1].type == "number" and stack[-2].type == "number":
                n2 = stack.pop()
                n1 = stack.pop()
                stack.append(dfv.data.Bool(n1.value <= n2.value))
            elif stack[-1].type == "integer" and stack[-2].type == "integer":
                n2 = stack.pop()
                n1 = stack.pop()
                stack.append(dfv.data.Bool(n1.value <= n2.value))
            elif stack[-1].type == "string" and stack[-2].type == "string":
                n2 = stack.pop()
                n1 = stack.pop()
                stack.append(dfv.data.Bool(n1.value <= n2.value))
            else:
                stack.append(dfv.data.Error("Types not supported"))
        else:
            stack.append(dfv.data.Error("Not enough parameters"))
            

class GreaterThan(Operator):
    def __init__(self):
        Operator.__init__(self)
        self.type = "greater_than"
        self.word = ">"
        
    def execute(self, stack, variables):
        if len(stack) >= 2:            
            if stack[-1].type == "number" and stack[-2].type == "number":
                n2 = stack.pop()
                n1 = stack.pop()
                stack.append(dfv.data.Bool(n1.value > n2.value))
            elif stack[-1].type == "integer" and stack[-2].type == "integer":
                n2 = stack.pop()
                n1 = stack.pop()
                stack.append(dfv.data.Bool(n1.value > n2.value))
            elif stack[-1].type == "string" and stack[-2].type == "string":
                n2 = stack.pop()
                n1 = stack.pop()
                stack.append(dfv.data.Bool(n1.value > n2.value))
            else:
                stack.append(dfv.data.Error("Types not supported"))
        else:
            stack.append(dfv.data.Error("Not enough parameters"))
            
class GreaterEqThan(Operator):
    def __init__(self):
        Operator.__init__(self)
        self.type = "greater_eq_than"
        self.word = ">="
        
    def execute(self, stack, variables):
        if len(stack) >= 2:            
            if stack[-1].type == "number" and stack[-2].type == "number":
                n2 = stack.pop()
                n1 = stack.pop()
                stack.append(dfv.data.Bool(n1.value >= n2.value))
            elif stack[-1].type == "integer" and stack[-2].type == "integer":
                n2 = stack.pop()
                n1 = stack.pop()
                stack.append(dfv.data.Bool(n1.value >= n2.value))
            elif stack[-1].type == "string" and stack[-2].type == "string":
                n2 = stack.pop()
                n1 = stack.pop()
                stack.append(dfv.data.Bool(n1.value >= n2.value))
            else:
                stack.append(dfv.data.Error("Types not supported"))
        else:
            stack.append(dfv.data.Error("Not enough parameters"))

            
class Quit(Operator):
    def __init__(self):
        Operator.__init__(self)
        self.type = "quit"
        self.word = "quit"
        
    def execute(self, stack, variables):
        variables["running"] = False
        
        
class Inc(Operator):
    def __init__(self):
        Operator.__init__(self)
        self.type = "inc"
        self.word = "++"
        
    def execute(self, stack, variables):
        if len(stack) >= 1:            
            if stack[-1].type == "number":
                n1 = stack.pop()
                stack.append(dfv.data.Number(n1.value + 1))
            elif stack[-1].type == "integer":
                n1 = stack.pop()
                stack.append(dfv.data.Integer(n1.value + 1))
            else:
                stack.append(dfv.data.Error("Types not supported"))
        else:
            stack.append(dfv.data.Error("Not enough parameters"))
            
            
class Dec(Operator):
    def __init__(self):
        Operator.__init__(self)
        self.type = "dec"
        self.word = "--"
        
    def execute(self, stack, variables):
        if len(stack) >= 1:            
            if stack[-1].type == "number":
                n1 = stack.pop()
                stack.append(dfv.data.Number(n1.value - 1))
            elif stack[-1].type == "integer":
                n1 = stack.pop()
                stack.append(dfv.data.Integer(n1.value - 1))
            else:
                stack.append(dfv.data.Error("Types not supported"))
        else:
            stack.append(dfv.data.Error("Not enough parameters"))
            
            
class Mod(Operator):
    def __init__(self):
        Operator.__init__(self)
        self.type = "mod"
        self.word = "%"
        
    def execute(self, stack, variables):
        if len(stack) >= 2:            
            if stack[-1].type == "number" and stack[-2].type == "number":
                n2 = stack.pop()
                n1 = stack.pop()
                stack.append(dfv.data.Number(int(n1.value) % int(n2.value)))
            if stack[-1].type == "integer" and stack[-2].type == "integer":
                n2 = stack.pop()
                n1 = stack.pop()
                stack.append(dfv.data.Integer((n1.value) % (n2.value)))
            else:
                stack.append(dfv.data.Error("Types not supported"))
        else:
            stack.append(dfv.data.Error("Not enough parameters"))
            

class And(Operator):
    def __init__(self):
        Operator.__init__(self)
        self.type = "and"
        self.word = "and"
        
    def execute(self, stack, variables):
        if len(stack) >= 2:            
            if stack[-1].type == "bool" and stack[-2].type == "bool":
                n2 = stack.pop()
                n1 = stack.pop()
                stack.append(dfv.data.Bool(n1.value and n2.value))
            else:
                stack.append(dfv.data.Error("Types not supported"))
        else:
            stack.append(dfv.data.Error("Not enough parameters"))
            
            
class Or(Operator):
    def __init__(self):
        Operator.__init__(self)
        self.type = "or"
        self.word = "or"
        
    def execute(self, stack, variables):
        if len(stack) >= 2:            
            if stack[-1].type == "bool" and stack[-2].type == "bool":
                n2 = stack.pop()
                n1 = stack.pop()
                stack.append(dfv.data.Bool(n1.value or n2.value))
            else:
                stack.append(dfv.data.Error("Types not supported"))
        else:
            stack.append(dfv.data.Error("Not enough parameters"))
            
            
class Ret(Operator):
    def __init__(self):
        Operator.__init__(self)
        self.type = "ret"
        self.word = "ret"
        
    def execute(self, stack, variables):
        variables["ret_function"] = True
        
        
class Print(Operator):
    def __init__(self):
        Operator.__init__(self)
        self.type = "print"
        self.word = "print"
        
    def execute(self, stack, variables):
        if len(stack) >= 1:            
            print stack.pop()
        else:
            stack.append(dfv.data.Error("Not enough parameters"))
            
            
class Vars(Operator):
    def __init__(self):
        Operator.__init__(self)
        self.type = "vars"
        self.word = "vars"
        
    def execute(self, stack, variables):
        gres = [key for key in variables]
        if variables["curr_function"] != None:
            ll = [key for key in variables["curr_function"].locals]
            gres.extend(ll)            
        res = [dfv.data.String(key) for key in gres]    
        stack.append(dfv.data.List(variables["curr_list"], values=res))
        
## Not implemented yet        
class Import(Operator):
    def __init__(self):
        Operator.__init__(self)
        self.type = "import"
        self.word = "import"
        
    def execute(self, stack, variables):
        if len(stack) >= 1:            
            if stack[-1].type == "string":
                n1 = stack.pop()
                #app.import_file()
            else:
                stack.append(dfv.data.Error("Types not supported"))
        else:
            stack.append(dfv.data.Error("Not enough parameters"))
            

class Type(Operator):
    def __init__(self):
        Operator.__init__(self)
        self.type = "type"
        self.word = "type"
        
    def execute(self, stack, variables):
        if len(stack) >= 3:            
            if stack[-3].type == "list" and stack[-2].type == "list" and stack[-1].type == "string":
                n3 = stack.pop()
                n2 = stack.pop()
                n1 = stack.pop()
                variables[n3.value] = dfv.data.Type(name=n3.value,
                                                    params=n1.values,
                                                    init_function=n2.values)
            else:
                stack.append(dfv.data.Error("Types not supported"))
        else:
            stack.append(dfv.data.Error("Not enough parameters"))
            
            
class Edit(Operator):
    def __init__(self):
        Operator.__init__(self)
        self.type = "edit"
        self.word = "edit"
        
    def execute(self, stack, variables):
        if len(stack) >= 1:            
            if stack[-1].type == "string":
                n1 = stack.pop()
                os.system("gedit %s &" % n1.value)
            else:
                stack.append(dfv.data.Error("Types not supported"))
        else:
            stack.append(dfv.data.Error("Not enough parameters"))
            
            
class Get(Operator):
    def __init__(self):
        Operator.__init__(self)
        self.type = "get"
        self.word = "get"
        
    def execute(self, stack, variables):
        if len(stack) >= 2:            
            if stack[-2].type.startswith("object") and stack[-1].type == "string":
                n2 = stack.pop()
                n1 = stack.pop()
                if n2.value in n1.locals:
                    stack.append(n1.locals[n2.value])
                else:
                    stack.append(dfv.data.Error("Variable %s not found in object" % n2.value))
            elif stack[-2].type == "list" and stack[-1].type == "integer":
                n2 = stack.pop()
                n1 = stack.pop()
                if n2.value < len(n1.values):
                    stack.append(n1.values[int(n2.value)])
                else:
                    stack.append(dfv.data.Error("Item %s not found in list" % n2.value))
            else:
                stack.append(dfv.data.Error("Types not supported"))
        else:
            stack.append(dfv.data.Error("Not enough parameters"))
            
            
class Swap(Operator):
    def __init__(self):
        Operator.__init__(self)
        self.type = "swap"
        self.word = "swap"
        
    def execute(self, stack, variables):
        if len(stack) >= 2:
            n2 = stack.pop()
            n1 = stack.pop()
            stack.append(n2)
            stack.append(n1)            
        else:
            stack.append(dfv.data.Error("Not enough parameters"))
            
            
class Who(Operator):
    def __init__(self):
        Operator.__init__(self)
        self.type = "who"
        self.word = "who"
        
    def execute(self, stack, variables):
        if len(stack) >= 1:
            n1 = stack.pop()
            stack.append(dfv.data.String(n1.type))            
        else:
            stack.append(dfv.data.Error("Not enough parameters"))
            
            
class Int(Operator):
    def __init__(self):
        Operator.__init__(self)
        self.type = "int"
        self.word = "int"
        
    def execute(self, stack, variables):
        if len(stack) >= 1:
            if stack[-1].type == "number":
                n1 = stack.pop()
                stack.append(dfv.data.Integer(int(n1.value))) 
            else:
                stack.append(dfv.data.Error("Types not supported"))           
        else:
            stack.append(dfv.data.Error("Not enough parameters"))
            

class Error(Operator):
    def __init__(self):
        Operator.__init__(self)
        self.type = "error"
        self.word = "error"
        
    def execute(self, stack, variables):
        if len(stack) >= 1:
            if stack[-1].type == "string":
                n1 = stack.pop()
                stack.append(dfv.data.Error(n1.value)) 
            else:
                stack.append(dfv.data.Error("Types not supported"))           
        else:
            stack.append(dfv.data.Error("Not enough parameters"))


class Pack(Operator):
    def __init__(self):
        Operator.__init__(self)
        self.type = "pack"
        self.word = "pack"
        
    def execute(self, stack, variables):
        if len(stack) >= 1:
            n1 = stack.pop()
            new_list = dfv.data.List(parent=variables["curr_list"], values=[n1])
            stack.append(new_list)
        else:
            stack.append(dfv.data.Error("Not enough parameters"))


class Npack(Operator):
    def __init__(self):
        Operator.__init__(self)
        self.type = "npack"
        self.word = "npack"
        
    def execute(self, stack, variables):
        if len(stack) >= 1:
            if stack[-1].type == "integer":
                n1 = stack.pop()
                if len(stack) >= n1.value:
                    new_list = dfv.data.List(parent=variables["curr_list"])
                    for k in range(n1.value):
                        new_list.append(stack.pop())
                    new_list.values.reverse()
                    stack.append(new_list)
                else:
                    stack.append(dfv.data.Error("Not enough parameters")) 
            else:
                stack.append(dfv.data.Error("Types not supported"))           
        else:
            stack.append(dfv.data.Error("Not enough parameters"))
            
            
class Unpack(Operator):
    def __init__(self):
        Operator.__init__(self)
        self.type = "unpack"
        self.word = "unpack"
        
    def execute(self, stack, variables):
        if len(stack) >= 1:
            if stack[-1].type == "list":
                n1 = stack.pop()
                for k in range(len(n1.values)):
                    stack.append(n1.values[k]) 
                stack.append(dfv.data.Integer(len(n1.values)))
            else:
                stack.append(dfv.data.Error("Types not supported"))           
        else:
            stack.append(dfv.data.Error("Not enough parameters"))
            
                