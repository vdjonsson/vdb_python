import pandas as pd
import seaborn as sb
import matplotlib.pyplot as plt

class Cluster:

    def __init__(self, args = 'from USA', cluster_name:str=None):

        self.args = args 

        # Open up socket to vdb and read in data from
        self.from_ = from_  # this is immutable for this cluster 
        self.data = self.get_vdb_data(command='from')
        self.cluster_name = cluster_name
        self.lineages_data = None
        self.trends_data = None
        self.frequencies_data = None 
        self.monthly_data = None
        self.weekly_data = None
        self.patterns_data = None
        self.consensus_data = None 
        #self.variants_data = None
        


        
    def from_ (self, location:str='world'):
        # location str:  example France + Japan
        
        self.data = get_vdb_data(command='from', command_args=location)        
        return self.data

    def patterns(self):
        self.patterns = get_vdb_data(command='patterns')
        return self.patterns 


    def read_csv(self, filename:str, header=None):
        tmp = pd.read_csv(filename, header=header)
        self.data = self.parse_data(tmp)

        
    def from_(self, location=str):

        from_country = self.data.Country == location
        from_state = self.data.Division == location
        values = from_state
        if from_country.sum()> from_state.sum():
            values = from_country

        self.data['from'] = values 
        return self.data[self.data['from']]

    ''' Listing commands '''
    def countries(self):
        ' Returns the list of countries represented in this cluster'        
        return list(self.data[self.data['from']].Country.unique())


    def states(self):
        ' Returns the list of states represented in this cluster'
        return list(self.data[self.data['from']].Division.unique())

    def lineages(self):
        ' Returns the list of lineages and their occurrences in the cluster '
        data = self.get_vdb_data(command='lineages')
        self.lineages_data = data


    def trends(self):
        ' Returns the list of lineages and their occurrences in the cluster '
        data = self.get_vdb_data(command='trends')
        self.trends_data = data



    def frequency(self):
        ' Returns the list of lineages and their occurrences in the cluster '
        data = self.get_vdb_data(command='freq')
        self.freq_data = data

    def weekly(self):
        ' Returns the list of lineages and their occurrences in the cluster '
        data = self.get_vdb_data(command='weekly')
        self.weekly_data = data
        
    def monthly(self):
        ' Returns the list of lineages and their occurrences in the cluster '
        data = self.get_vdb_data(command='monthly')
        self.monthly_data = data
    

    def clusters(self):
        print('clusters() function: Not implemented')

    def proteins(self):
        print('proteins() function : Not implemented')
        
    def variants (self):
        data = self.get_vdb_data(command='variants')
        self.variants_data = data


    ''' Commands for mutation patterns '''
    def consensus(self):
        data = self.get_vdb_data(command='consensus')
        self.consensus_data = data


    def patterns(self):
        data = self.get_vdb_data(command='patterns')
        self.patterns_data = data



    ''' Plotting functions '''

    def plot (self,command='from', groupby=None, logy=False):

        if command == 'from':
            # Todo implement heatmap of mutations per virus
            # Cluster by groupby
            if groupby == 'state':
                groupby = 'Division' 
            grouped = self.data.groupby(groupby).count().reset_index()

            plt.figure(figsize=(10,3))
            sb.set(context='paper', font_scale=1, style='ticks')
            sb.barplot(data=grouped, x= groupby, y='Isolate')
            plt.title(command + ': ' + self.from_ + ' grouped by:' + groupby)
            plt.ylabel('Count, Isolates')
            plt.xticks(rotation=90)

        elif command == 'patterns':
            print('Patterns from ', self.from_ , ':', self.patterns_data.values[0][0])
        elif command == 'consensus':
            print('Consensus from ', self.from_, ':', self.consensus_data.values[0][0])
        elif command == 'lineages':

            plt.figure(figsize=(10,3))
            sb.set(context='paper', font_scale=1, style='ticks')
            sb.barplot(data=self.lineages_data, x= 'Lineage', y='Count')
            if logy:
                plt.semilogy()
            plt.title(command + ': ' + self.from_ + ' lineages')
            plt.ylabel('Count, Lineages')
            plt.xticks(rotation=90)
            
            #print(self.lineages_data)
        elif command == 'trends':
            data = self.trends_data.set_index('Time')
            plt.figure(figsize=(10,3))
            sb.set(context='paper', font_scale=1, style='ticks')
            sb.lineplot(data=data.iloc[:,0:5])
            plt.title(command + ': ' + self.from_ + ' top 5')
            plt.ylabel('Frequency, Lineages')
            plt.xticks(rotation=90)
        elif command in  ['frequencies', 'freq']:

            sb.set(context='paper', font_scale=1, style='ticks')
            sb.barplot(data=self.freq_data, x='Mutation', y='Frequency')
            plt.title(command + ': ' + self.from_)
            plt.ylabel('Frequency, Mutations')
            plt.xticks(rotation=90)
            
        elif command == 'weekly':

            data = self.weekly_data.set_index('Time')
            plt.figure(figsize=(10,3))
            sb.set(context='paper', font_scale=1, style='ticks')
            sb.lineplot(data=data)
            plt.title(command + ': ' + self.from_ )
            plt.ylabel('Count, Lineages')
            plt.xticks(rotation=90)

        elif command == 'monthly':
            data = self.monthly_data.set_index('Time')
            plt.figure(figsize=(10,3))
            sb.set(context='paper', font_scale=1, style='ticks')
            sb.lineplot(data=data)
            plt.title(command + ': ' + self.from_ )
            plt.ylabel('Count, Lineages')
            plt.xticks(rotation=90)
        elif command == 'variants':

            sb.set(context='paper', font_scale=1, style='ticks')
            sb.barplot(data=self.variants_data, x= 'Lineage', y='Count')
            if logy:
                plt.semilogy()
            plt.title(command + ': ' + self.from_ + ' Count')
            plt.ylabel('Count, Variants')
            plt.xticks(rotation=90)

            sb.set(context='paper', font_scale=1, style='ticks')
            sb.barplot(data=self.variants_data, x= 'Variant', y='Count')
            if logy:
                plt.semilogy()
            plt.title(command + ': ' + self.from_ + ' Count')
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
 


