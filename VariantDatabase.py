import subprocess
import sys
import time
import pandas as pd
import io as io 
import os
import pty


workingDirectory ='/Users/vanessajonsson/Google Drive/data/rep/vdb_python-main/'
vdbPath ='/Users/vanessajonsson/Google Drive/data/rep/vdb_python-main/v27_new'
stdbufPath ='/Users/vanessajonsson/Google Drive/data/rep/vdb_python-main/stdbuf-osx-master/stdbuf'

class VariantDatabase(object):


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
        return self.instance


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
        return trimmed.decode("utf-8")


    def get_data (self,command, saveto):

        print('GETDATA', command, saveto) 
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
    

    def parse_data_lineages(self, data):
        
        ''' Parses lineages data '''
        labels = ['Lineage', 'Count']
        data.iloc[:,2] = data.iloc[:,2].str[1:]
        data.iloc[:,127] = data.iloc[:,127].str[:-1]
        data = data.rename(columns=dict(zip([0,1], labels)))

        return data


    def parse_data_trends(self, data):
        ''' Parses trends data '''
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
