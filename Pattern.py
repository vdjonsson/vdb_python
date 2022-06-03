import pandas as pd
import seaborn as sb
import matplotlib.pyplot as plt
import VariantDatabase as vd
import readline

import inspect
from random import randrange

class Pattern:
    def __init__(self, command:str, pattern_name:str='', verbose=None, indirect=False):
        self.command = command
        self.vdb = vd.VariantDatabase()
        self.pattern_name = pattern_name

        if verbose == None:
            if self.vdb.verbose == True:
                self.verbose = True
            if self.vdb.verbose == False:
                self.verbose = False
        else:
            self.verbose = verbose

        if len(self.pattern_name) == 0:
            nameFromDeclaration = self.patternNameFromDeclaration(indirect = indirect)
            if len(nameFromDeclaration) > 0:
                self.pattern_name = nameFromDeclaration
            else:
                self.pattern_name = self.vdb.nextAnonName()
#                print("Pattern name missing")
                print("Anonymous pattern named " + self.pattern_name)
                
        command = self.pattern_name + " = " + command
        self.data = self.vdb.command(command)
        parts = self.data.split(" as ")
        self.mutations = []
        if len(parts) > 1:
            self.mutations = parts[1].split()
        
        if self.verbose:
            print(self.data)
             
        self.lineages_data = None
        self.trends_data = None
        self.frequencies_data = None 
        self.monthly_data = None
        self.weekly_data = None
        self.patterns_data = None
        self.consensus_data = None 
        self.subpatterns = dict()
           

    def info(self):
        print('---- Pattern ----')
        print('Name:', self.pattern_name)
        print('Definition:', self.command)
        print('Mutations:', self.mutations)

        if len(self.subpatterns) > 0 :
            print('---- Subpattern ----')
            for c in self.subpatterns.values():
                c.info()
            
    def patternNameFromDeclaration(self, indirect=False):
        if not indirect:
            previous_frame = inspect.currentframe().f_back.f_back
        else:
            previous_frame = inspect.currentframe().f_back.f_back.f_back
        (_,_,_,lines,_) = inspect.getframeinfo(previous_frame)
        
        if lines != None:
            line = lines[0]
        else:
            line = readline.get_history_item(readline.get_current_history_length())
            if line == None:
                return ""

        nameStart = -1
        nameEnd = -1
        equalsFound = 0
        closeParen = 0
        dotAfterFound = False
        for i in range(len(line)):
            if equalsFound == 0:
                if nameStart == -1 and line[i] != " ":
                    nameStart = i
                if nameStart != -1 and nameEnd == -1 and (line[i] == " " or line[i] == "="):
                    nameEnd = i
            if line[i] == "=":
                equalsFound += 1
            if line[i] == ")":
                closeParen += 1
            if line[i] == "#":
                break
            if closeParen > 0 and line[i] == ".":
                dotAfterFound = True
        assignment = nameStart != -1 and nameEnd != -1 and equalsFound > 0 and not dotAfterFound
        if assignment:
            return line[nameStart:nameEnd]
        return ""

    def tmpName(self):
        return "tmp" + str(randrange(10000000))

    def __add__(self, other):
        nameFromDeclaration = self.patternNameFromDeclaration()
        cmd = self.pattern_name + " + " + other.pattern_name
        return Pattern(cmd, pattern_name=nameFromDeclaration)

    def __sub__(self, other):
        nameFromDeclaration = self.patternNameFromDeclaration()
        cmd = self.pattern_name + " - " + other.pattern_name
        return Pattern(cmd, pattern_name=nameFromDeclaration)

    def __and__(self, other):
        nameFromDeclaration = self.patternNameFromDeclaration()
        cmd = self.pattern_name + " * " + other.pattern_name
        return Pattern(cmd, pattern_name=nameFromDeclaration)

    def __eq__(self,other):
        cmd = self.pattern_name + " == " + other.pattern_name
        result = self.vdb.command(cmd)
        rlen = len(result)
        if rlen > 4:
            if result[rlen-4] == "1":
                return True
            elif result[rlen-4] == "0":
                return False
        return None

    @property
    def count(self):
        return int(vd.V("count "+self.pattern_name).split()[3].replace(",",""))

    def __len__(self):
        return self.count
        
    def __str__(self):
        return ' '.join(self.mutations)
