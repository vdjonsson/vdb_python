import pandas as pd
import seaborn as sb
import matplotlib.pyplot as plt
import VariantDatabase as vd

import inspect
from random import randrange

class Cluster:
    def __init__(self, command:str,cluster_name:str='', verbose:bool=False):
        self.command = command
             
        self.vdb = vd.VariantDatabase()
        self.cluster_name = cluster_name
        
        if len(cluster_name) == 0:
             nameFromDeclaration = self.clusterNameFromDeclaration()
        if len(nameFromDeclaration) > 0:
            self.cluster_name = nameFromDeclaration
            command = nameFromDeclaration + " = " + command

        self.data = self.vdb.command(command)

        if verbose:
            print(self.data)
             
        self.lineages_data = None
        self.trends_data = None
        self.frequencies_data = None 
        self.monthly_data = None
        self.weekly_data = None
        self.patterns_data = None
        self.consensus_data = None 
        #self.variants_data = None
           

    def clusterNameFromDeclaration(self):
        previous_frame = inspect.currentframe().f_back.f_back
        (_,_,_,lines,_) = inspect.getframeinfo(previous_frame)
        parts = lines[0].split()
        assignment = False
        if parts[1] == "=":
            # need to parse lines[0] to verify that declaration is assigning a cluster
            assignment = True
        if assignment:
            return (parts[0])
        return ""

    def tmpName(self):
        return "tmp" + str(randrange(10000000))


    ''' Listing commands '''
    def countries(self):
        ' Returns the list of countries represented in this cluster'        
        return list(self.data.Country.unique())


    def states(self):
        ' Returns the list of states represented in this cluster'
        return list(self.data.Division.unique())

    def lineages(self):
        ' Returns the list of lineages and their occurrences in the cluster '
        tmpName = self.tmpName()
        self.vdb.command(tmpName+"=lineages "+self.cluster_name)
        self.lineages_data = self.vdb.command("save "+tmpName+" -")
        self.vdb.command("clear "+tmpName)


    def trends(self):
        ' Returns the list of lineages and their occurrences in the cluster '
        
        data = self.vdb.command(command = 'trends', args= '', cluster_name = 'x',saveto='trends_x.csv')
        self.trends_data = data



    def frequency(self):
        ' Returns the list of lineages and their occurrences in the cluster '
        data = self.vdb.command(command = 'freq', args= '', cluster_name = 'x',saveto='freq_x.csv')
        self.freq_data = data

    def weekly(self):
        ' Returns the list of lineages and their occurrences in the cluster '
        data = self.vdb.command(command = 'weekly', args= '', cluster_name = 'x',saveto='weekly_x.csv')
        self.weekly_data = data
        
    def monthly(self):
        ' Returns the list of lineages and their occurrences in the cluster '
        data = self.vdb.command(command = 'monthly', args= '', cluster_name = 'x',saveto='monthly_x.csv')
        self.monthly_data = data
    

    def clusters(self):
        print('clusters() function: Not implemented')

    def proteins(self):
        print('proteins() function : Not implemented')
        
    def variants (self):
        data = self.vdb.command(command = 'variants', args= '', cluster_name = '',saveto='variants.csv')
        self.variants_data = data


    ''' Commands for mutation patterns '''
    def consensus(self):
        data = self.vdb.command(command = 'consensus', args= '', cluster_name = 'x',saveto='consensus.csv')
        self.consensus_data = data


    def patterns(self):
        data = self.vdb.command(command = 'patterns', args= '', cluster_name = 'x',saveto='patterns.csv')
        self.patterns_data = data



    ''' Plotting functions '''

    def plot (self,command='from', groupby=None, logy=False, top=20):

        if command == 'from':
            # Todo implement heatmap of mutations per virus

            if groupby == 'state':
                groupby = 'Division'

            print(self.data.Division.unique()) 
            grouped = self.data.groupby(groupby).count().reset_index()

            print(grouped) 
            plt.figure(figsize=(10,3))
            sb.set(context='paper', font_scale=1, style='ticks')
            sb.barplot(data=grouped, x= groupby, y='Isolate')
            if logy:
                plt.semilogy()
            plt.title(command + ': ' + self.args + ' grouped by:' + groupby)
            plt.ylabel('Count, Isolates')
            plt.xticks(rotation=90)

        elif command == 'patterns':
            print('Patterns from ', self.args, ':', self.patterns_data.values[0][0])
        elif command == 'consensus':
            print('Consensus from ', self.args, ':', self.consensus_data.values[0][0])
        elif command == 'lineages':

            plt.figure(figsize=(10,3))
            sb.set(context='paper', font_scale=1, style='ticks')
            sb.barplot(data=self.lineages_data.iloc[0:top,:], x= 'Lineage', y='Count')
            if logy:
                plt.semilogy()
            plt.title(command + ': ' + self.args + ' lineages')
            plt.ylabel('Count, Lineages')
            plt.xticks(rotation=90)
            
            #print(self.lineages_data)
        elif command == 'trends':
            data = self.trends_data.set_index('Time')
            plt.figure(figsize=(10,3))
            sb.set(context='paper', font_scale=1, style='ticks')
            sb.lineplot(data=data.iloc[:,0:top])
            plt.title(command + ': ' + self.args )
            plt.ylabel('Frequency, Lineages')
            plt.xticks(rotation=90)
        elif command in  ['frequencies', 'freq']:

            sb.set(context='paper', font_scale=1, style='ticks')
            sb.barplot(data=self.freq_data, x='Mutation', y='Frequency')
            plt.title(command + ': ' + self.args)
            plt.ylabel('Frequency, Mutations')
            plt.xticks(rotation=90)
            
        elif command == 'weekly':

            data = self.weekly_data.set_index('Time')
            plt.figure(figsize=(10,3))
            sb.set(context='paper', font_scale=1, style='ticks')
            sb.lineplot(data=data)
            plt.title(command + ': ' + self.args )
            plt.ylabel('Count, Lineages')
            plt.xticks(rotation=90)

        elif command == 'monthly':
            data = self.monthly_data.set_index('Time')
            plt.figure(figsize=(10,3))
            sb.set(context='paper', font_scale=1, style='ticks')
            sb.lineplot(data=data)
            plt.title(command + ': ' + self.args )
            plt.ylabel('Count, Lineages')
            plt.xticks(rotation=90)
        elif command == 'variants':

            sb.set(context='paper', font_scale=1, style='ticks')
            sb.barplot(data=self.variants_data, x= 'Lineage', y='Count')
            if logy:
                plt.semilogy()
            plt.title(command + ': ' + self.args + ' Count')
            plt.ylabel('Count, Variants')
            plt.xticks(rotation=90)

            sb.set(context='paper', font_scale=1, style='ticks')
            sb.barplot(data=self.variants_data, x= 'Variant', y='Count')
            if logy:
                plt.semilogy()
            plt.title(command + ': ' + self.args + ' Count')
            plt.ylabel('Count, Variants')
            plt.xticks(rotation=90)



    ''' Filtering commands ''' 
    def containing(self, pattern:list=None):
        return 

    def notcontaining(self, pattern:list=None):
        return

    def before(self, date:str=None):
        return

    def after(self, date:str=None):
        return

    def range(self, dates:str=None):
        return

    def lessthan(self, num_mutations:int=None):
        return
    
    def morethan(self, num_mutations:int=None):
        return

    def sample(self, num_mutations:int=None):
        return 
 

