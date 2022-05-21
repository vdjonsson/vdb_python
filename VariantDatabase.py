import subprocess
import sys
import time
import pandas as pd
import io as io 


class VariantDatabase:

    __instance = None
    @staticmethod 
    def getInstance():
        if VariantDatabase.__instance == None:
            print('No instance of Variant Database created')
        return VariantDatabase.__instance

  
    def __init__(self, path:str, working_dir:str):

        if VariantDatabase.__instance != None:
            raise Exception("This class is a singleton!")
        
        else:
         
            self.path = path
            self.working_dir = working_dir 
            self.input_buffer = sys.stdin  
            self.output_buffer = subprocess.PIPE

            self.proc = subprocess.Popen(
                args=[path],
                stdin=subprocess.PIPE,  # pipe its STDIN so we can write to it
                stdout= sys.stdout, # pipe directly to the output_buffer
                cwd=working_dir,
                universal_newlines=True, shell=True)
            VariantDatabase.__instance = self

            
    def concatenate_commands(self, commands:list):

        str_comm = commands[2] + '= ' + commands[0] + ' ' + commands[1] + ' \n save ' + commands[2] + ' ' + commands[3] + ' \n exit \n'
        
        return str_comm

    
    def command(self, command:str, args:str, cluster_name:str, saveto:str):

        print('Sending ', command, ' to vdb')
        print("Input: ", end="", file=self.proc.stdout, flush=True)  # print the input prompt    
        print(self.concatenate_commands([command,args,cluster_name, saveto]) , file=self.proc.stdin, flush=True)  

        x = self.proc.stdout

        data = self.get_data(command, saveto)
        self.terminate()
        
        return data

    def terminate(self): 
        self.proc.terminate()


    def get_data (self,command, saveto):

        print('get_data', command, saveto) 
        data = pd.DataFrame()
        header = None
        skiprows =[0]

        if command in ['consensus', 'patterns']:
            skiprows = None

        if command == 'trends':
            header = 'infer'

        tmp = pd.read_csv(self.working_dir + saveto, header=header, skiprows =skiprows)
        data = self.parse_data(tmp, command = command)        
        return data


    def parse_data_from(self, data):
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
    

    def parse_data_lineages(self, data):

        labels = ['Lineage', 'Count']
        data.iloc[:,2] = data.iloc[:,2].str[1:]
        data.iloc[:,127] = data.iloc[:,127].str[:-1]
        data = data.rename(columns=dict(zip([0,1], labels)))

        return data


    def parse_data_trends(self, data):

        labels = ['Time']
        data = data.rename(columns=dict(zip([data.columns[0]], labels)))
        return data

    def parse_data_freq(self, data):
            
        labels = ['Mutation', 'Frequency']
        data = data.rename(columns=dict(zip(data.columns, labels)))

        return data

    def parse_data_weekly_monthly(self, data):
        labels = ['Time', 'Count']
        data = data.rename(columns=dict(zip(data.columns, labels)))
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

        if command == 'from': 
            tmp  = self.parse_data_from(data)
        elif command =='lineages':
            tmp = self.parse_data_lineages(data)
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
            
        return tmp
