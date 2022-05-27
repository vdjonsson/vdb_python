import pandas as pd
import seaborn as sb
import matplotlib.pyplot as plt
import VariantDatabase as vd

import inspect
from random import randrange

class Cluster:
    def __init__(self, command:str, cluster_name:str='', verbose=None):
        self.command = command
        self.vdb = vd.VariantDatabase()
        self.cluster_name = cluster_name # APW
        self.verbose = False # APW 
        if verbose == None:
            if self.vdb.verbose == True:
                self.verbose = True
            if self.vdb.verbose == False:
                self.verbose = False

        if len(cluster_name) == 0:
            nameFromDeclaration = self.clusterNameFromDeclaration()
            if len(nameFromDeclaration) > 0:
                self.cluster_name = nameFromDeclaration
                command = nameFromDeclaration + " = " + command
            else:
                print("Cluster name missing")
        else:
            command = self.cluster_name + " = " + command

        self.data = self.vdb.command(command)

        if self.verbose:
            print(self.data)
             
        self.lineages_data = None
        self.trends_data = None
        self.frequencies_data = None 
        self.monthly_data = None
        self.weekly_data = None
        self.patterns_data = None
        self.consensus_data = None 
        self.subclusters = dict()
           

    def info(self):
        print('---- Cluster ----')
        print('Name:', self.cluster_name)
        print('Definition:', self.command)
        print('Num. clusters:', len(self.subclusters))

        if len(self.subclusters) > 0 :
            print('---- Subcluster ----')
            for c in self.subclusters.values():
                c.info()
            
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

    @property
    def count(self):
        return int(vd.V("count "+self.cluster_name).split()[3].replace(",",""))

    def __len__(self):
        return self.count

    ''' Listing commands '''
    def countries(self):
        
        ' Returns the list of countries represented in this cluster'
        tmpName = self.tmpName()

        self.vdb.command(tmpName+"=countries "+self.cluster_name)        
        out = self.vdb.command("save "+tmpName+" -")
        self.countries_data = self.vdb.parse_data(out, 'countries')
        print(self.countries_data)
        self.vdb.command("clear "+tmpName)

    def states(self):
        
        ' Returns the list of states represented in this cluster'

        tmpName = self.tmpName()

        self.vdb.command(tmpName+"=states "+self.cluster_name)        
        out = self.vdb.command("save "+tmpName+" -")
        self.states_data = self.vdb.parse_data(out, 'states')
        self.vdb.command("clear "+tmpName)
        return self.states_data

    def lineages(self):
        
        ' Returns the list of lineages and their occurrences in the cluster '

        tmpName = self.tmpName()
        self.vdb.command(tmpName+"=lineages "+self.cluster_name)        
        out = self.vdb.command("save "+tmpName+" -")
        self.lineages_data = self.vdb.parse_data(out, 'lineages')
        self.vdb.command("clear "+tmpName)


    def trends(self):
        
        ' Returns the list of lineages and their trends '        
        tmpName = self.tmpName()
        self.vdb.command(tmpName+"=trends "+self.cluster_name)
        out = self.vdb.command("save "+tmpName+" -")
        self.trends_data = self.vdb.parse_data(out, 'trends')
        print(self.trends_data)
        self.vdb.command("clear "+tmpName)
        


    def frequency(self):
        
        ' Returns the list of lineages and their occurrences in the cluster '

        tmpName = self.tmpName()
        self.vdb.command(tmpName+"=freq "+self.cluster_name)
        out = self.vdb.command("save "+tmpName+" -")
        self.freq_data = self.vdb.parse_data(out, 'freq')
    
        self.vdb.command("clear "+tmpName)


    def weekly(self):
        ' Returns the list of lineages and their occurrences in the cluster '

        tmpName = self.tmpName()
        self.vdb.command(tmpName+"=weekly "+self.cluster_name)
        out = self.vdb.command("save "+tmpName+" -")

        self.weekly_data = self.vdb.parse_data(out, 'weekly')

        print(self.weekly_data)

        self.vdb.command("clear "+tmpName)

        
    def monthly(self):
        
        ' Returns the list of lineages and their occurrences in the cluster '

        tmpName = self.tmpName()
        self.vdb.command(tmpName+"=monthly "+self.cluster_name)
        out = self.vdb.command("save "+tmpName+" -")

        self.monthly_data = self.vdb.parse_data(out, 'monthly')

        self.vdb.command("clear "+tmpName)


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

    def plot (self,command='from', groupby=None, logy=False, top=5):

        title = command + ', Cluster:' + self.cluster_name + ' Command:'+ self.command
        
        if command == 'from':
            # Todo implement heatmap of mutations per virus

            if groupby == 'state':
                groupby = 'Division'

            print(self.data.Division.unique()) 
            grouped = self.data.groupby(groupby).count().reset_index()

            plt.figure(figsize=(10,3))
            sb.set(context='paper', font_scale=1, style='ticks')
            sb.barplot(data=grouped, x= groupby, y='Isolate')
            if logy:
                plt.semilogy()
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
            if logy:
                plt.semilogy()

            plt.ylabel('Count, Lineages')
            plt.xticks(rotation=90)

        elif command == 'countries':
            sb.set(context='paper', font_scale=1, style='ticks')
            sb.barplot(data=self.countries_data,x= 'Country',y='Count')
            if logy:
                plt.semilogy()

            plt.ylabel('Count')
            plt.xticks(rotation=90)

        elif command == 'states':
            sb.set(context='paper', font_scale=1, style='ticks')
            sb.barplot(data=self.states_data,x= 'State',y='Count')
            if logy:
                plt.semilogy()
            plt.ylabel('Count')
            plt.xticks(rotation=90)

        elif command == 'trends':

            ''' Plot over time with lineages ''' 
            plt.figure(figsize=(10,3))
            sb.set(context='paper', font_scale=1, style='ticks')
            sb.lineplot(data =self.trends_data.iloc[:,0:top])

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
            if logy:
                plt.semilogy()

            plt.ylabel('Count, Variants')
            plt.xticks(rotation=90)

            sb.set(context='paper', font_scale=1, style='ticks')
            sb.barplot(data=self.variants_data, x= 'Variant', y='Count')
            if logy:
                plt.semilogy()

            plt.ylabel('Count, Variants')
            plt.xticks(rotation=90)

        plt.title(title)

    ''' Filtering commands ''' 
    def containing(self, pattern:list,str=None):

        pattern_str = pattern

        if isinstance(pattern, list):
            pattern_str = ''
            for p in pattern:
                pattern_str = pattern_str + p + ' '

        command = self.cluster_name + ' containing ' + pattern_str
        cluster = Cluster(command = command)
        #self.subclusters[cluster.cluster_name] = cluster #APW
        
        if self.verbose:
            print(command)
            print(cluster.data)
            
        return cluster

    def notcontaining(self, pattern:list,str=None):

        pattern_str = pattern

        if isinstance(pattern, list):
            pattern_str = ''
            for p in pattern:
                pattern_str = pattern_str + p + ' '

        command = self.cluster_name + ' not containing ' + pattern_str
        cluster = Cluster(command = command)
        #self.subclusters[cluster.cluster_name] = cluster
        
        if self.verbose:
            print(command)
            print(cluster.data)
            
        return cluster


    def before(self, date:str=None):

        command = self.cluster_name + ' before ' + date
        print(command)
        cluster = Cluster(command = command)
        #self.subclusters[cluster.cluster_name] = cluster
        # Create new cluster here and return it
        if self.verbose:
            print(command)
            print(cluster.data)
            
        return cluster


    def after(self, date:str=None):
        
        command = self.cluster_name + ' after ' + date
        print(command) 
        cluster = Cluster(command = command)
        #self.subclusters[cluster.cluster_name] = cluster
        # Create new cluster here and return it
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
        print('COMMAND')
        print(command)
        cluster = Cluster(command = command)
        #self.subclusters[cluster.cluster_name] = cluster
        
        if self.verbose:
            print(command)
            print(cluster.data)
            
        return cluster


    def lessthan(self, num_mutations:int=None):
        
        command = self.cluster_name + ' < ' + num_mutations
        cluster = Cluster(command = command)
        #self.subclusters[cluster.cluster_name] = cluster
        if self.verbose:
            print(command)
            print(cluster.data)
            
        return cluster

    
    def morethan(self, num_mutations:int=None):
        
        command = self.cluster_name + ' > ' + num_mutations
        
        cluster = Cluster(command = command)
        #self.subclusters[cluster.cluster_name] = cluster
        if self.verbose:
            print(command)
            print(cluster.data)
            
        return cluster

    def named(self, state_id:str=None, epi_id:str=None) :
        arg= state_id 
        if state_id == None:
            arg = epi_id
            
        command = self.cluster_name + ' named ' + arg
        cluster = Cluster(command = command)
        #self.subclusters[cluster.cluster_name] = cluster
        
        if self.verbose:
            print(command)
            print(cluster.data)
            
        return cluster


    def lineage(self, pango_lineage:str):
        
        command = self.cluster_name + ' lineage ' + pango_lineage
        cluster = Cluster(command = command)
        #self.subclusters[cluster.cluster_name] = cluster
        
        if self.verbose:
            print(command)
            print(cluster.data)
            
        return cluster

    def sample(self, fraction:float=None):

        command = self.cluster_name + ' sample ' + str(fraction)
        cluster = Cluster(command = command)
        
        #self.subclusters[cluster.cluster_name] = cluster

        if self.verbose:
            print(command)
            print(cluster.data)
            
        return cluster



