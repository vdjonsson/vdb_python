import pandas as pd
import seaborn as sb
import matplotlib.pyplot as plt
import VariantDatabase as vd
import Pattern as pat
import readline
import numpy.random as np 
import sys

import inspect
from random import randrange

class Cluster:
    def __init__(self, command:str, cluster_name:str='', verbose=None, indirect=False):
        self.command = command
        self.vdb = vd.VariantDatabase()
        self.cluster_name = cluster_name
        
        if verbose == None:
            if self.vdb.verbose == True:
                self.verbose = True
            if self.vdb.verbose == False:
                self.verbose = False
        else:
            self.verbose = verbose

        if len(self.cluster_name) == 0:
            nameFromDeclaration = self.clusterNameFromDeclaration(indirect = indirect)
            if len(nameFromDeclaration) > 0:
                self.cluster_name = nameFromDeclaration
            else:
                self.cluster_name = self.vdb.nextAnonName()
                print("Anonymous cluster named " + self.cluster_name)
                
        if self.cluster_name != "world":
            command = self.cluster_name + " = " + command
            self.data = self.vdb.command(command)
        else:
            self.data = "world cluster defined"
            
        if self.verbose:
            print(self.data)

        self.vdb.update_clusters(command=command)
             
        self.lineages_data = None
        self.trends_data = None
        self.frequencies_data = None 
        self.monthly_data = None
        self.weekly_data = None
        self.patterns_data = None
        self.consensus_data = None 
        self.subclusters = dict()
        self.default_plot_args = {'context':'paper',
                                  'figsize':(10,3), 'linewidth':1.5,
                                  'save':False,
                                  'save_dir':'./output/','dpi':150,
                                  'show':True, 
                                  'logy':False,
                                  'top':5}

                                  

    def info(self):
        print('---- Cluster ----')
        print('Name:', self.cluster_name)
        print('Definition:', self.command)
        print('Number of isolates: ', "{:,}".format(self.count))
        print('Num. subclusters:', len(self.subclusters))

        if len(self.subclusters) > 0 :
            print('---- Subcluster ----')
            for c in self.subclusters.values():
                c.info()
            
    def clusterNameFromDeclaration(self, indirect=False):
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
        nameFromDeclaration = self.clusterNameFromDeclaration()
        cmd = self.cluster_name + " + " + other.cluster_name
        return Cluster(cmd, cluster_name=nameFromDeclaration)

    def __sub__(self, other):
        nameFromDeclaration = self.clusterNameFromDeclaration()
        cmd = self.cluster_name + " - " + other.cluster_name
        return Cluster(cmd, cluster_name=nameFromDeclaration)

    def __and__(self, other):
        nameFromDeclaration = self.clusterNameFromDeclaration()
        cmd = self.cluster_name + " * " + other.cluster_name
        return Cluster(cmd, cluster_name=nameFromDeclaration)

    def __eq__(self,other):
        cmd = self.cluster_name + " == " + other.cluster_name
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
        return int(vd.V("count "+self.cluster_name).split()[3].replace(",",""))

    def __len__(self):
        return self.count

    ''' Listing commands '''
    def countries(self, plot:bool=False, plot_args:dict=None):
        
        ' Returns the list of countries represented in this cluster'
        tmpName = self.tmpName()

        self.vdb.command(tmpName+"=countries "+self.cluster_name)        
        out = self.vdb.command("save "+tmpName+" -")
        self.countries_data = self.vdb.parse_data(out, 'countries')
        self.vdb.command("clear "+tmpName)
        return self.countries_data

    def states(self, plot:bool=False, plot_args:dict=None):
        
        ' Returns the list of states represented in this cluster'

        tmpName = self.tmpName()

        self.vdb.command(tmpName+"=states "+self.cluster_name)        
        out = self.vdb.command("save "+tmpName+" -")
        self.states_data = self.vdb.parse_data(out, 'states')
        self.vdb.command("clear "+tmpName)
        return self.states_data

    def lineages(self, plot:bool=False, plot_args:dict=None):
        
        ' Returns the list of lineages and their occurrences in the cluster '

        tmpName = self.tmpName()
        self.vdb.command(tmpName+"=lineages "+self.cluster_name)        
        out = self.vdb.command("save "+tmpName+" -")
        self.lineages_data = self.vdb.parse_data(out, 'lineages')
        self.vdb.command("clear "+tmpName)
        return self.lineages_data

    def trends(self, plot:bool=False, plot_args:dict=None):
        
        ' Returns the list of lineages and their trends '        
        tmpName = self.tmpName()
        self.vdb.command(tmpName+"=trends "+self.cluster_name)
        out = self.vdb.command("save "+tmpName+" -")
        self.trends_data = self.vdb.parse_data(out, 'trends')
        self.vdb.command("clear "+tmpName)
        if plot:
            self.plot('trends',args = plot_args)
        return self.trends_data


    def frequency(self, plot:bool=False, plot_args:dict=None):
        
        ' Returns the list of lineages and their occurrences in the cluster '

        tmpName = self.tmpName()
        self.vdb.command(tmpName+"=freq "+self.cluster_name)
        out = self.vdb.command("save "+tmpName+" -")
        self.freq_data = self.vdb.parse_data(out, 'freq')
    
        self.vdb.command("clear "+tmpName)
        
        if plot:
            self.plot(command='freq', args=plot_args)
            
        return self.freq_data


    def weekly(self, plot:bool=False, plot_args:dict=None):
        ' Returns the list of lineages and their occurrences in the cluster '

        tmpName = self.tmpName()
        self.vdb.command(tmpName+"=weekly "+self.cluster_name)
        out = self.vdb.command("save "+tmpName+" -")

        self.weekly_data = self.vdb.parse_data(out, 'weekly')
        self.vdb.command("clear "+tmpName)
        if plot:
            self.plot(command='weekly', args=plot_args)
        return self.weekly_data

        
    def monthly(self, plot:bool=False, plot_args:dict=None):
        
        ' Returns the list of lineages and their occurrences in the cluster '

        tmpName = self.tmpName()
        self.vdb.command(tmpName+"=monthly "+self.cluster_name)
        out = self.vdb.command("save "+tmpName+" -")

        self.monthly_data = self.vdb.parse_data(out, 'monthly')
        self.vdb.command("clear "+tmpName)
        if plot:
            self.plot(command='monthly', args=plot_args)
        return self.monthly_data


    def clusters(self):
        print('clusters() function: Not implemented')

    def proteins(self):
        print('proteins() function : Not implemented')
        
    def variants (self):
        data = self.vdb.command(command = 'variants', args= '', cluster_name = '',saveto='variants.csv')
        self.variants_data = data
        return self.variants_data 

    ''' Commands for mutation patterns '''
    def consensus(self):#APW set consensus?

        command = 'consensus ' + self.cluster_name
        pattern = pat.Pattern(command = command, indirect = True)
        return pattern


    def patterns(self): #APW set patterns?
        
        command = 'patterns ' + self.cluster_name
        pattern = pat.Pattern(command = command, indirect = True)
        return pattern  


    ''' Plotting functions '''

    
    def plot (self,command:str='from', groupby:str=None, logy:bool=None, top:int=None, save:bool=None,show:bool=None, dpi:int=None, save_dir:str=None, save_file:str=None, figsize=None, linewidth=None, args:dict=None):

        title = command.upper() + '\n Cluster: ' + self.cluster_name + ' \n Cluster Definition: '+ self.command
    
        if args == None:
            args = self.default_plot_args

        if logy==None: logy = self.default_plot_args['logy']
        if top==None: top = self.default_plot_args['top']
        if save==None: save = self.default_plot_args['save']
        if save: 
            if save_dir==None: save_dir = self.default_plot_args['save_dir']
            if save_file==None: save_file = command + '_' + str(np.rand()) + '.png'
        if show==None: show = self.default_plot_args['show']
        if dpi==None: dpi = self.default_plot_args['dpi']
        if figsize==None: show = self.default_plot_args['figsize']
        if linewidth==None: linewidth = self.default_plot_args['linewidth']
        
        
        sb.set(context=self.default_plot_args['context'])
        if command == 'from':
            if groupby == 'state':
                groupby = 'Division'

            grouped = self.data.groupby(groupby).count().reset_index()

            plt.figure(figsize=(10,3))
            sb.set(context='paper', font_scale=1, style='ticks')
            sb.barplot(data=grouped, x= groupby, y='Isolate')
            plt.title(title   + ' grouped by:' + groupby)
            plt.ylabel('Count, Isolates')
            plt.xticks(rotation=90)

        elif command == 'patterns':
            print('Patterns from ', ':', self.patterns_data.values[0][0])
            
        elif command == 'consensus':
            print('Consensus from ',  ':', self.consensus_data.values[0][0])
            
        elif command == 'lineages':
            sb.set(context='paper', font_scale=1, style='ticks')
            sb.barplot(data=self.lineages_data.iloc[0:top,:], x= 'Lineage', y='Count')
            plt.ylabel('Count, Lineages')
            plt.xticks(rotation=90)

        elif command == 'countries':
            sb.set(context='paper', font_scale=1, style='ticks')
            sb.barplot(data=self.countries_data,x= 'Country',y='Count')
            plt.ylabel('Count')
            plt.xticks(rotation=90)

        elif command == 'states':
            sb.set(context='paper', font_scale=1, style='ticks')
            sb.barplot(data=self.states_data,x= 'State',y='Count')
            plt.ylabel('Count')
            plt.xticks(rotation=90)

        elif command == 'trends':

            ''' Plot over time with lineages ''' 
            plt.figure(figsize=figsize)
            sb.set(context='paper', font_scale=1, style='ticks')
            sb.lineplot(data =self.trends_data.iloc[:,0:top], lw=linewidth)
            plt.ylabel('Frequency, Lineages')
            plt.xticks(rotation=90)
            
            
        elif command in  ['frequencies', 'freq']:
            
            sb.set(context='paper', font_scale=1, style='ticks')
            sb.barplot(data=self.freq_data.iloc[0:top,:], x='Mutation', y='Frequency')
            plt.ylabel('Frequency, Mutations')
            plt.xticks(rotation=90)
            
            
        elif command == 'weekly':

            plt.figure(figsize=(10,3))
            sb.set(context='paper', font_scale=1, style='ticks')
            sb.lineplot(data=self.weekly_data)
            plt.ylabel('Count, Lineages')
            plt.xticks(rotation=90)

        elif command == 'monthly':

            plt.figure(figsize=(10,3))
            sb.set(context='paper', font_scale=1, style='ticks')
            sb.lineplot(data=self.monthly_data)

            plt.ylabel('Count, Lineages')
            plt.xticks(rotation=90)
        elif command == 'variants':

            sb.set(context='paper', font_scale=1, style='ticks')
            sb.barplot(data=self.variants_data, x= 'Lineage', y='Count')
            plt.ylabel('Count, Variants')
            plt.xticks(rotation=90)

            sb.set(context='paper', font_scale=1, style='ticks')
            sb.barplot(data=self.variants_data, x= 'Variant', y='Count')
            plt.ylabel('Count, Variants')
            plt.xticks(rotation=90)

        if logy:
            plt.semilogy()
            
        plt.title(title)
        plt.tight_layout()
        
        if save:
            plt.savefig(save_dir + save_file, dpi=dpi)
        if show: 
            plt.show()

    ''' Filtering commands ''' 
    def containing(self, pattern:list,str=None):

        pattern_str = pattern
        if isinstance(pattern, list):
            pattern_str = ''
            for p in pattern:
                pattern_str = pattern_str + p + ' '
        elif isinstance(pattern, pat.Pattern):
            print(pattern)
            pattern_str = pattern.__str__()

        command = self.cluster_name + ' containing ' + pattern_str
        cluster = Cluster(command = command, indirect = True)
        self.subclusters[cluster.cluster_name] = cluster 

        return cluster

    def notcontaining(self, pattern:list,str=None):

        pattern_str = pattern
        if isinstance(pattern, list):
            pattern_str = ''
            for p in pattern:
                pattern_str = pattern_str + p + ' '
        elif isinstance(pattern, pat.Pattern):
            print(pattern)
            pattern_str = pattern.__str__()

        command = self.cluster_name + ' not containing ' + pattern_str
        cluster = Cluster(command = command, indirect = True)
        self.subclusters[cluster.cluster_name] = cluster 
                    
        return cluster


    def before(self, date:str=None):

        command = self.cluster_name + ' before ' + date
        print(command)
        cluster = Cluster(command = command, indirect = True)
        self.subclusters[cluster.cluster_name] = cluster

        if self.verbose:
            print(command)
            print(cluster.data)
            
        return cluster


    def after(self, date:str=None):
        
        command = self.cluster_name + ' after ' + date
        print(command) 
        cluster = Cluster(command = command, indirect = True)
        self.subclusters[cluster.cluster_name] = cluster

        if self.verbose:
            print(command)
            print(cluster.data)
            
        return cluster


    def range(self, dates:list,str=None):
        pattern_str = dates

        if isinstance(dates, list):
            pattern_str = ''
            for p in dates:
                pattern_str = pattern_str + p + '-'

            pattern_str=pattern_str[:-1]

        command = self.cluster_name + ' range ' + pattern_str
        cluster = Cluster(command = command, indirect = True)
        self.subclusters[cluster.cluster_name] = cluster
        
        if self.verbose:
            print(command)
            print(cluster.data)
            
        return cluster


    def lessthan(self, num_mutations:int=None):
        
        command = self.cluster_name + ' < ' + num_mutations
        cluster = Cluster(command = command, indirect = True)
        self.subclusters[cluster.cluster_name] = cluster
        if self.verbose:
            print(command)
            print(cluster.data)
            
        return cluster

    
    def greaterthan(self, num_mutations:int=None):
        
        command = self.cluster_name + ' > ' + num_mutations
        cluster = Cluster(command = command, indirect = True)
        self.subclusters[cluster.cluster_name] = cluster
        if self.verbose:
            print(command)
            print(cluster.data)
            
        return cluster

    def named(self, state_id:str=None, epi_id:str=None) :
        arg= state_id 
        if state_id == None:
            arg = epi_id
            
        command = self.cluster_name + ' named ' + arg
        cluster = Cluster(command = command, indirect = True)
        self.subclusters[cluster.cluster_name] = cluster
        
        if self.verbose:
            print(command)
            print(cluster.data)
            
        return cluster


    def lineage(self, pango_lineage:str):
        
        command = self.cluster_name + ' lineage ' + pango_lineage
        cluster = Cluster(command = command, indirect = True)
        self.subclusters[cluster.cluster_name] = cluster
        
        if self.verbose:
            print(command)
            print(cluster.data)
            
        return cluster

    def sample(self, fraction:float=None):

        command = self.cluster_name + ' sample ' + str(fraction)
        cluster = Cluster(command = command, indirect = True)
        self.subclusters[cluster.cluster_name] = cluster

        if self.verbose:
            print(command)
            print(cluster.data)
            
        return cluster


def diff(item1,item2):
    name1 = ""
    name2 = ""
    if isinstance(item1, Cluster):
        name1 = item1.cluster_name
    elif isinstance(item1, pat.Pattern):
        name1 = item1.pattern_name
    if isinstance(item2, Cluster):
        name2 = item2.cluster_name
    elif isinstance(item2, pat.Pattern):
        name2 = item2.pattern_name
    if len(name1) > 0 and len(name2) > 0:
        command = "diff " + name1 + " " + name2
        diffInfo = vd.VariantDatabase().command(command)
        print(diffInfo)
