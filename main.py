#! /usr/bin/python
# -*- coding=utf-8 -*-

import math
import dfv.data
import dfv.operator
import re
import matplotlib.pyplot as plt
import logging
import os
import sys

def is_number(string):
    try:
        float(string)
        return True
    except:
        return False 

COMMAND = """
{startup.ee}
"""
            
class App:
    TEXT = """
PyCalc v0.1
           """
    def __init__(self):
        self.cmd = ""
        self.vars = {"running": True,
                     "curr_list": None,
                     "curr_function": None,
                     "ret_function": False,
                     "[": dfv.operator.StartList(),
                     "]": dfv.operator.EndList(),
                     "+": dfv.operator.Sum(),
                     "-": dfv.operator.Diff(),
                     "*": dfv.operator.Mult(),
                     "/": dfv.operator.Div(),
                     "//": dfv.operator.IntDiv(),
                     "drop": dfv.operator.Drop(),
                     "..": dfv.operator.Drop(),
                     "dup": dfv.operator.Dup(),
                     ".": dfv.operator.Dup(),
                     "exp": dfv.operator.Exp(),
                     "neg": dfv.operator.Neg(),
                     "inv": dfv.operator.Inv(),
                     "complex": dfv.operator.ToComplex(),
                     "sin": dfv.operator.Sin(),
                     "asin": dfv.operator.Asin(),
                     "cos": dfv.operator.Cos(),
                     "acos": dfv.operator.Acos(),
                     "tan": dfv.operator.Tan(),
                     "atan": dfv.operator.Atan(),
                     "atan2": dfv.operator.Atan2(),
                     "ln": dfv.operator.Ln(),
                     "abs": dfv.operator.Abs(),
                     "arg": dfv.operator.Arg(),
                     "pow": dfv.operator.Pow(),
                     "def": dfv.operator.Def(),
                     "cls": dfv.operator.Cls(),
                     "eval": dfv.operator.Eval(),
                     "fun": dfv.operator.Fun(),
                     "cat": dfv.operator.Cat(),
                     "pi": dfv.data.Number(math.pi),
                     "e": dfv.data.Number(math.e),
                     "true": dfv.data.Bool(True),
                     "false": dfv.data.Bool(False),
                     "if": dfv.operator.If(),
                     "ifelse": dfv.operator.IfElse(),
                     "not": dfv.operator.Not(), 
                     "while": dfv.operator.While(),
                     "=": dfv.operator.Eq(),
                     "quit": dfv.operator.Quit(),
                     "!=": dfv.operator.Neq(),
                     "<": dfv.operator.LessThan(),
                     "<=": dfv.operator.LessEqThan(),
                     ">": dfv.operator.GreaterThan(),
                     ">=": dfv.operator.GreaterEqThan(),
                     "++": dfv.operator.Inc(),
                     "--": dfv.operator.Dec(),
                     "%": dfv.operator.Mod(),
                     "and": dfv.operator.And(),
                     "or": dfv.operator.Or(),
                     "ret": dfv.operator.Ret(),
                     "print": dfv.operator.Print(),
                     "vars": dfv.operator.Vars(),
                     "type": dfv.operator.Type(),
                     "edit": dfv.operator.Edit(),
                     "get": dfv.operator.Get(),
                     "swap": dfv.operator.Swap(),
                     "who": dfv.operator.Who(),
                     "int": dfv.operator.Int(),
                     "_": dfv.operator.Int(),
                     "error": dfv.operator.Error(),
                     "pack": dfv.operator.Pack(),
                     "npack": dfv.operator.Npack(),
                     "unpack": dfv.operator.Unpack(),
                     "real": dfv.operator.ToReal(),
                     "set": dfv.operator.Set()}
                     
        self.string_mode = False
        self.stack = dfv.data.List(parent=None)
        self.curr_list = self.stack
        
    def run(self):
        print(self.TEXT)
        
        #while self.cmd != "quit":
        self.execute_cmds(self.parse_cmd(COMMAND))
        while self.vars["running"]:
            #self.print_stack()
            self.print_list()
            self.cmd = raw_input(">> ")
            self.execute_cmds(self.parse_cmd(self.cmd))
        return 0
                
    def execute_cmds(self, cmds):
        for cmd in cmds:
            if self.vars["curr_list"] == None:
                cmd.execute(self.stack, self.vars)                
            else:
                if cmd.value != "]" and cmd.value != "[": self.vars["curr_list"].append(cmd)
                else: cmd.execute(self.stack, self.vars)                
                
    def parse_cmd(self, cmd_string):
        cmds = []
        cmd_string = re.sub('#([^"]*)#', "", cmd_string)
        strs = re.findall('"([^"]*)"', cmd_string)
        cmd_string = re.sub('"([^"]*)"', " $str ", cmd_string)
        imports = re.findall('{([^}]+)}', cmd_string)
        cmd_string = re.sub('{([^}]+)}', " $imp ", cmd_string)
        cmd_string = cmd_string.replace("[", " [ ")
        cmd_string = cmd_string.replace("]", " ] ")
        for cmd in str.split(cmd_string):
            if is_number(cmd):
                if "." in cmd:
                    cmds.append(dfv.data.Number(float(cmd)))
                else:
                    cmds.append(dfv.data.Integer(int(cmd)))
            elif cmd == "$str":
                cmds.append(dfv.data.String(strs.pop(0)))
            elif cmd == "$imp":
                try:
                    path = os.path.dirname(os.path.abspath(__file__)) + "/" + imports.pop(0)
                    with open(path, "r") as f:
                        lines = f.read()
                    cmds.extend(self.parse_cmd(lines))
                except:
                    pass
                    #cmds.append(dfv.data.String(strs.pop(0)))
            else:
                cmds.append(dfv.data.Cmd(cmd))
        return cmds
        
    def print_list(self):
        self.stack.print_()
        
    def print_stack(self):
        print "----------------"
        for x in self.stack:
            print "%s : %s" % (x, x.type)
        print "----------------"
        
    def import_file(self, filename):
        with open(filename, "r") as f:
            lines = f.read()
        self.execute_cmds(self.parse_cmd(lines))

def main():    
    path = os.path.dirname(os.path.abspath(__file__))
    logging.basicConfig(filename=path + '/log/log.log', level=logging.DEBUG)
    app = App()
    app.run()
    
if __name__ == "__main__": main()