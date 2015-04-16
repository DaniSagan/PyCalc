#! /usr/bin/python
# -*- coding=utf-8 -*-

import math
import dfv.data
import dfv.operator
import re
import logging
import os
import readline
readline.parse_and_bind("tab: complete")


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
Daniel Fernández Villanueva, ©2014
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
                     "list:!": dfv.operator.Eval(),
                     "pyeval": dfv.operator.PyEval(),
                     "pyexec": dfv.operator.PyExec(),
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
                     "for": dfv.operator.For(),
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
                     "lget": dfv.operator.LGet(),
                     "swap": dfv.operator.Swap(),
                     "who": dfv.operator.Who(),
                     "int": dfv.operator.Int(),
                     "_": dfv.operator.Int(),
                     "error": dfv.operator.Error(),
                     "pack": dfv.operator.Pack(),
                     "npack": dfv.operator.Npack(),
                     "unpack": dfv.operator.Unpack(),
                     "real": dfv.operator.ToReal(),
                     "set": dfv.operator.Set(),
                     "tostring": dfv.operator.ToString(),
                     "extract": dfv.operator.Extract()}

        self.string_mode = False
        self.stack = dfv.data.List(parent=None)
        self.curr_list = self.stack

    def run(self):
        print(self.TEXT)
        self.execute_cmds(self.parse_cmd(COMMAND))
        readline.set_completer(self.complete)

        while self.vars["running"]:
            #self.print_stack()
            self.print_list()
            self.cmd = raw_input(">> ")
            self.execute_cmds(self.parse_cmd(self.cmd))
            print ""
        return 0

    def execute_cmds(self, cmds):
        for cmd in cmds:
            """if (len(self.stack) >= 1 and self.stack[-1].type == "error" and
               cmd.value != "cls" and cmd.value != "quit"):
                break"""
            if self.vars["curr_list"] == None:
                try:
                    cmd.execute(self.stack, self.vars)
                except ValueError:
                    self.stack.append(dfv.data.Error("Math domain error"))
            else:
                if cmd.value != "]" and cmd.value != "[" or cmd.type == "string":
                    self.vars["curr_list"].append(cmd)
                else:
                    try:
                        cmd.execute(self.stack, self.vars)
                    except ValueError:
                        self.stack.append(dfv.data.Error("Math domain error"))


    def parse_cmd(self, cmd_string):
        cmds = []

        # check for comments and delete them
        cmd_string = re.sub('#([^#]*)#', "", cmd_string)

        # check for strings
        strs = re.findall('"([^"]*)"', cmd_string)
        cmd_string = re.sub('"([^"]*)"', " $str ", cmd_string)



        # check for imports
        imports = re.findall('{([^}]+)}', cmd_string)
        cmd_string = re.sub('{([^}]+)}', " $imp ", cmd_string)

        # lists
        cmd_string = cmd_string.replace("[", " [ ")
        cmd_string = cmd_string.replace("]", " ] ")

        #print cmd_string

        for cmd in str.split(cmd_string):
            if is_number(cmd):
                if "." in cmd:
                    cmds.append(dfv.data.Number(float(cmd)))
                else:
                    cmds.append(dfv.data.Integer(int(cmd)))
            elif cmd == "true":
                cmds.append(dfv.data.Bool(True))
            elif cmd == "false":
                cmds.append(dfv.data.Bool(False))
            elif cmd == "$str":
                cmds.append(dfv.data.String(strs.pop(0)))
            elif cmd == "$imp":
                path = os.path.dirname(os.path.abspath(__file__)) + "/" + imports.pop(0)
                try:
                    with open(path, "r") as f:
                        lines = f.read()
                    cmds.extend(self.parse_cmd(lines))
                    #cmds[0:0] = self.parse_cmd(lines)
                except:
                    cmds.append(dfv.data.Error("Could not load module at location %s" % path))
            else:
                cmds.append(dfv.data.Cmd(cmd))
        return cmds

    def print_list(self):
        self.stack.print_()

    def print_stack(self):
        print "----------------"
        for x in self.stack:
            print "%s :\t\t%s" % (x, x.type)
        print "----------------"

    def import_file(self, filename):
        with open(filename, "r") as f:
            lines = f.read()
        self.execute_cmds(self.parse_cmd(lines))

    def complete(self, text, state):
        v = [key for key in self.vars if ":" not in key]
        last_type = None
        if len(self.stack) >= 1:
            last_type = self.stack[-1].type
            if last_type.startswith("object."): last_type = last_type[7:]
            v_obj = [key.split(":")[1] for key in self.vars if key.startswith(last_type + ":")]
            v = v + v_obj
        results = [x + " " for x in v if x.startswith(text)]
        return results[state]

def main():
    path = os.path.dirname(os.path.abspath(__file__))
    if not os.path.exists(path + '/log'):
        os.makedirs(path + '/log')
    if not os.path.exists(path + '/script'):
        os.makedirs(path + '/script')
    logging.basicConfig(filename=path + '/log/log.log', level=logging.DEBUG)

    app = App()
    app.run()

if __name__ == "__main__": main()
