import Cluster as cd
import VariantDatabase as vd
import matplotlib.pyplot as plt

path = '/Users/vanessajonsson/Google\ Drive/data/rep/vdb-main/v27_new'
working_dir = '/Users/vanessajonsson/Google Drive/data/rep/vdb-main/'

vdb = vd.VariantDatabase(path, working_dir)

x  = cd.Cluster(cluster_name = 'x', command = 'from', args='CA', saveto='fromCA.csv')

x.plot('from',groupby='state')
plt.tight_layout()
plt.show()

x.patterns()
x.plot('patterns')

x.lineages()
print(x.lineages_data)
x.plot('lineages', logy=True, top=20)
plt.tight_layout()
plt.show()

x.trends()
print(x.trends_data)
x.plot('trends', logy=True, top=5)
plt.tight_layout()
plt.show()

x.weekly()
x.plot('weekly', logy=True)
plt.tight_layout()
plt.show()

x.monthly()
x.plot('monthly', logy=True)
plt.tight_layout()
plt.show()
