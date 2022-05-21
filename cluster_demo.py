import vdb as vd
import inspect
from random import randrange

class Cluster:

    def __init__(self, command:str, args:str="", cluster_name:str="", saveto:str=None, verbose:bool=False):

        self.command = command
        self.cluster_name = cluster_name
        self.args = args
        self.saveto=saveto 

        self.vdb = vd.VariantDatabase()
#        print('VDB Path:', vd.vdbPath)


        if len(cluster_name) == 0:
            nameFromDeclaration = self.clusterNameFromDeclaration()
            if len(nameFromDeclaration) > 0:
                self.cluster_name = nameFromDeclaration
                command = nameFromDeclaration + " = " + command

#        self.data = self.vdb.command(command = command, args= args, cluster_name = cluster_name,saveto=saveto)
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
#        data = self.vdb.command(command = 'lineages', args= '', cluster_name = 'x',saveto='lineages_x.csv')
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
 


# demo of Cluster class

x = Cluster("from ca",verbose=True)
y = Cluster("x after 1/1/22",verbose=True)
z = Cluster("B.1.1.7 from ny before 10/1/22",verbose=True)
y.lineages()
print("y.lineages_data = "+y.lineages_data)
