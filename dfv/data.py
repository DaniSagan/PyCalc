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
            elif variables[self.value].type == "data_type":
                variables[self.value].execute(stack, variables, parent_function)
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

class Type(Data):
    def __init__(self, name, params, functions):
        Data.__init__(self)
        self.type = "data_type"
        self.name = name
        self.params = params
        self.functions = functions
    
    def execute(self, stack, variables, parent_function):
        #self.locals = {}
        
        if len(stack) >= len(self.params):
            param_names = [p.value for p in self.params]
            param_values = []
            for p in param_names:
                param_values.append(stack.pop())
            param_values.reverse()
            new_obj = Object(_type=self.name, name="", params=self.params, param_values=param_values, functions=self.functions)
            """variables["curr_function"] = new_obj
            for cmd in self.init_function:
                #print "cmd:", cmd
                cmd.execute(stack, variables, parent_function=new_obj)           
                if variables["ret_function"]: break
            variables["ret_function"] = False
            variables["curr_function"] = parent_function"""
            stack.append(new_obj)
        else:
            stack.append(Error("Not enough parameneters"))
        
    def __str__(self):
        return "%s : type" % (self.name)
    
class Object(Data):
    def __init__(self, _type, name, params, param_values, functions):
        Data.__init__(self)
        self.type = _type
        self.name = name
        self.locals = {}
        for p, v in zip(params, param_values):
            self.locals[p] = v
    
    def execute(self, stack, variables, parent_function):
        pass
        
    def __str__(self):
        return "[%s] : object" % (" ".join([("%s: %s"%(key, self.locals[key])) for key in self.locals]))
    
    
    