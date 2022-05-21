import VariantDatabase as vd



path = '/Users/vanessajonsson/Google\ Drive/data/rep/vdb-main/v27_new'
working_dir = '/Users/vanessajonsson/Google Drive/data/rep/vdb-main/'

vdb = vd.VariantDatabase(path, working_dir)

data = vdb.command(command = 'from', args= 'US', cluster_name = 'x',saveto='usa.csv')

print(data)

''' Singleton class test '''
vdb_error = vd.VariantDatabase(path, working_dir)

