import subprocess
import sys
import time
import pandas as pd
import io as io 
import os
import pty


workingDirectory = "/Users/apw/Downloads/latest7/"
vdbPath = "/Users/apw/Downloads/latest7/vdb"
stdbufPath = "/Users/apw/Downloads/latest7/stdbuf"

workingDirectory ='/Users/vanessajonsson/Google Drive/data/rep/vdb_python-main/'
vdbPath ='/Users/vanessajonsson/Google Drive/data/rep/vdb_python-main/v27_new'
stdbufPath ='/Users/vanessajonsson/Google Drive/data/rep/vdb_python-main/stdbuf-osx-master/stdbuf'

class VariantDatabase(object):

    anonCounter = 0

    def __new__(self):
        if not hasattr(self, 'instance'):
            self.instance = super(VariantDatabase, self).__new__(self)
            input_buffer = sys.stdin
            output_buffer = sys.stdout
            self.stdout_primary_fd, self.stdout_secondary_fd = pty.openpty()
            self.proc = subprocess.Popen([stdbufPath,"-o0",vdbPath],
                            stdin=subprocess.PIPE,           
                            stdout=self.stdout_secondary_fd, 
                            cwd=workingDirectory,
                            universal_newlines=True,
                            bufsize=0)

            self.clusters = dict()
            
            print("Starting vdb...")
            loadingOutput = self.command(self,"",init=True)
            for x in range(len(loadingOutput)):
                if loadingOutput[x] == "E" and loadingOutput[x+1] == "n" and loadingOutput[x+2] == "t":
                    break
            loadingOutput = loadingOutput[:x-5]
            print(loadingOutput)
            self.command(self,"displayTextWithColor off")
            self.command(self,"paging off")
            self.command(self,"quiet on")
            self.command(self,"listAccession on")
            self.verbose = False

        return self.instance

    def is_cluster_command(self, command):
        cluster_commands = ['containing', 'notcontaining', 'before', 'after','range','lessthan','greaterthan','named','lineage', 'sample']
        for c in cluster_commands :
            if c in command:
                return True
        return False

    def existing_cluster(self, cluster_name):
        return cluster_name in list(self.clusters)

    def parse_parent_cluster(self, command):
        command_parsed = command.split(' ')
        if self.is_cluster_command(command):
            return command_parsed[2], command_parsed[0]
        else:
            return command_parsed[0], None

    def update_clusters(self,command:str=None):

        parent, child = self.parse_parent_cluster(command)
        
        if self.existing_cluster(parent):    
            children = self.clusters[parent]
            if child !=None: 
                self.clusters[parent] = children.append(child)
                self.clusters[parent] = children
            else:
                print('Warning: cluster', parent,'and all children will be deleted')
                print('and replaced by', command)
                del self.clusters[parent]
                self.clusters[parent] = []
        else:
            self.clusters[parent] = []



    def command(self,command,init=False):
        
        ''' Executes vdb command and returns output in a string '''
        
        if not init:
            print(command, file=self.proc.stdin, flush=True)
        output = bytes()
        foundVDB = False
        while True:
            output += os.read(self.stdout_primary_fd, 10000)
            for x1 in range(len(output)):
                if output[x1] == 10:    # linefeed
                    break
            for x2 in range(len(output)):
                if output[x2] == 118 and output[x2+1] == 100 and output[x2+2] == 98 and output[x2+3] == 62: 
                    foundVDB = True
                    break
            if foundVDB:
                break
        trimmed = output[x1+1:x2-1]

        out  = trimmed.decode("utf-8")

        return out


            
    def groupVariants(self):
        self.command("group variants")
        
    def nextAnonName(self):
        self.anonCounter += 1
        return "anon" + str(self.anonCounter)
    
    def parse_data_from(self, data):
        
        ''' Parses cluster data returned in from command ''' 
        tmp  = data.iloc[:,0].str.split(pat='|', expand=True)
        tmp.iloc[:,0] = data.iloc[:,0].str[1:]
        labels = ['Isolate','Virus ID', 'Date_collection']
        tmp = tmp.rename(columns=dict(zip([0,1,2], labels)))
        tmp['Pattern'] = data.iloc[:,1]
        tmp.drop(columns=[3], inplace=True)

        splits = tmp.Isolate.str.split(pat='/',expand=True)
        tmp['Country']= splits.iloc[:,0]
        tmp['Division']= splits.iloc[:,1].str.split(pat='-', expand=True).iloc[:,0]
        tmp['from'] = True # do not filter unless specified 

        return tmp
    

    def parse_data_lineages(self, data, query_type='Lineage'):
        
        ''' Parses lineages data '''
        data = pd.read_csv(io.StringIO(data), sep="\n").iloc[:,0].str.split(',', expand=True)
        end = len(data.columns)-1
        labels = [query_type, 'Count']
        data.iloc[:,2] = data.iloc[:,2].str[1:]
        data.iloc[:,end] = data.iloc[:,end].str[:-1]
        data = data.rename(columns=dict(zip([0,1], labels)))
        data = data.iloc[0:data.shape[0]-1,:]
        data = data.set_index(query_type)
        data = data.astype(float)
        data = data.reset_index(query_type)

        return data


    def parse_data_trends(self, data):

        ''' Parses trends data '''
        data = pd.read_csv(io.StringIO(data), sep="\n", header='infer', skiprows=[0]).iloc[0:-1,0].str.split(',', expand=True)

        labels = list(data.iloc[0,:].values)

        data = data.iloc[1:,:]
        data.columns = labels
        data = data.set_index('Month')
        data = data.astype(float)

        return data


    def parse_data_freq(self, data):

        data = pd.read_csv(io.StringIO(data), sep="\n", header='infer', skiprows=[0]).iloc[0:-1,0].str.split(',', expand=True)


        labels = ['Mutation', 'Frequency']
        data = data.rename(columns=dict(zip(data.columns, labels)))
        data = data.set_index('Mutation')
        data = data.astype(float)
        data = data.reset_index('Mutation')
        return data


    def parse_data_weekly_monthly(self, data):

        ''' Parses trends data '''
        data = pd.read_csv(io.StringIO(data), sep="\n", header='infer', skiprows=[0]).iloc[0:-1,0].str.split(',', expand=True)

        
        labels = ['Date', 'Count']
        data = data.rename(columns=dict(zip(data.columns, labels)))
        data = data.set_index('Date')
        data = data.astype(float)
    
        return data

    def parse_data_patterns(self, data):
        labels = ['Mutations']
        data = data.rename(columns=dict(zip(data.columns, labels)))
        return data

    def parse_data_variants(self, data):
        labels = ['Variant', 'Lineage', 'Count']
        data = data.rename(columns=dict(zip(data.columns, labels)))
        return data
        
    def parse_data(self, data, command='from'):

        tmp = data 
        if 'from' in command:
            #tmp  = self.parse_data_from(data)
            print('parse data on cluster not implemented')
        elif command =='trends':
            tmp = self.parse_data_trends(data)
        elif command == 'freq':
            tmp = self.parse_data_freq(data)
        elif command in ['weekly', 'monthly']:
            tmp = self.parse_data_weekly_monthly(data)
        elif command in ['patterns', 'consensus']:
            tmp = self.parse_data_patterns(data)
        elif command == 'variants':
            tmp = self.parse_data_variants(data)
        elif command in ['states', 'countries', 'lineages']:
            labels = dict(zip(['states', 'countries', 'lineages'], ['State', 'Country', 'Lineage']))
            tmp = self.parse_data_lineages(data, query_type=labels[command])
        return tmp

def v(cmd:str):
    print(VariantDatabase().command(cmd))

def V(cmd:str):
    return VariantDatabase().command(cmd)
