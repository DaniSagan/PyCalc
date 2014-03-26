#! /usr/bin/python
# -*- coding=utf-8 -*-

        
class Data:
    def __init__(self):
        self.category = "data"
        self.type = "none"
        self.value = "none"
        #self.basic = True
        
    def __str__(self):
        return self.value
        
    def execute(self, stack, variables, parent_function=None):
        stack.append(self)


class Cmd(Data):
    def __init__(self, value):
        Data.__init__(self)
        self.type = "cmd"
        self.value = value
    
    def execute(self, stack, variables, parent_function=None):
        # first we see if we can match the command to any global variable
        if self.value in variables:
            if variables[self.value].type == "function":
                fn = Function(variables[self.value].values, variables[self.value].name)
                fn.execute(stack, variables, parent_function)
                #variables[self.value].execute(stack, variables, parent_function) 
            else:
                variables[self.value].execute(stack, variables)                
        # if not we try the local variables
        # if we're not inside a function there are no local variables
        elif variables["curr_function"] != None and self.value in variables["curr_function"].locals:
            if variables["curr_function"].locals[self.value].type == "function":
                variables["curr_function"].locals[self.value].execute(stack, variables, parent_function=variables["curr_function"])    
            else: 
                variables["curr_function"].locals[self.value].execute(stack, variables)
        else:
            stack.append(Error("Command \"%s\" not found" % self.value))
        
    def __str__(self):
        return "%s : %s" % (self.value, self.type)


class String(Data):
    def __init__(self, value):
        Data.__init__(self)
        self.type = "string"
        self.value = value
        
    def __str__(self):
        return "\"%s\" : %s" % (self.value, self.type)
                
        
class Number(Data):
    def __init__(self, value):
        Data.__init__(self)
        self.type = "number"
        self.value = value
        
    def __str__(self):
        return str(self.value) + " : " + self.type
        

class Bool(Data):
    def __init__(self, value):
        Data.__init__(self)
        self.type = "bool"
        self.value = value
        
    def __str__(self):
        return "%s : %s" % (self.value, self.type)


class Error(Data):
    def __init__(self, value):
        Data.__init__(self)
        self.type = "error"
        self.value = value
        
    def __str__(self):
        return "Error: " + self.value

        
class Complex(Data):
    def __init__(self, real_value, imag_value):
        Data.__init__(self)
        self.type = "complex"
        self.real_value = real_value
        self.imag_value = imag_value
        
    def __str__(self):
        res = ""
        if self.real_value != 0: res += str(self.real_value)
        if self.imag_value >= 0: res += "+" + str(self.imag_value) + "i"
        else: res += (str(self.imag_value) + "i")
        res += " : " + self.type
        return res
        

class List(Data):
    def __init__(self, parent, values=None):
        Data.__init__(self)
        self.type = "list"
        self.parent = parent
        self.values = []
        if values != None: self.values.extend(values)
        
    def append(self, value):
        self.values.append(value)
        
    def pop(self):
        return self.values.pop()
        
    def print_(self):
        print "-------------------"
        for x in self.values:
            print x
        print "-------------------"
        
    def __str__(self):
        return "[ %s ] : list" % ", ".join([str(x) for x in self.values])
        
    def __len__(self):
        return len(self.values)
        
    def __getitem__(self, k):
        return self.values[k]

        
class Function(Data):
    def __init__(self, values, name):
        Data.__init__(self)
        self.type = "function"
        self.values = values
        self.name = name
        self.locals = {}
    
    def execute(self, stack, variables, parent_function):
        #self.locals = {}
        variables["curr_function"] = self
        for cmd in self.values:
            #print "cmd:", cmd
            cmd.execute(stack, variables, parent_function=self)           
            if variables["ret_function"]: break
        variables["ret_function"] = False
        variables["curr_function"] = parent_function
        
    def __str__(self):
        return "%s: [ %s ] : function" % (self.name, ", ".join([str(x) for x in self.values]))