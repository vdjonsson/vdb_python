import Cluster as c 
import matplotlib.pyplot as plt


''' Unit test for this class ''' 
x = c.Cluster("from ca",cluster_name ='x',verbose=True)
y = c.Cluster("x after 12/1/20",verbose=True)
z = c.Cluster("B.1.1.7 from ny before 10/1/22",verbose=True)
a = c.Cluster('from France + Japan', verbose=True)
z= c.Cluster('from US', verbose=True)

x.info()


#a.countries()
#print(a.countries_data)
#a.plot('countries',logy=True)
#plt.tight_layout()
#plt.show()

#a.frequency()
#print(a.freq_data)
#a.plot('freq',logy=True, top=10)
#plt.tight_layout()
#plt.show()

nca = a.notcontaining('E484K N501Y') # OR nca = a.notcontaining(['E484K', 'N501Y'])
print(nca)
nca.info()


ca = a.containing('E484K N501Y') # OR ca = a.containing(['E484K', 'N501Y'])

ca.frequency()
print(ca.freq_data) 
ca.plot('freq',logy=True, top=10)
plt.tight_layout()
plt.show()


#s = z.named('CA') #APW 
s = z.lineage('B.1.1')


z.info() 

z.trends()
z.plot('trends',logy=True, top=5)
plt.tight_layout()
plt.show()


s = z.sample(0.38)
s.trends()
s.plot('trends', logy=True, top=5)
s.info()

s.frequency()
s.plot('freq',logy=True, top=10)
plt.tight_layout()
plt.show()


aa = a.range('6/1/2020-8/1/2020') # OR
s = a.range(['6/1/2020','8/1/2020'])

o = a.after('4/1/2022')
o.frequency()
o.plot('freq',logy=True, top=10)
plt.tight_layout()
plt.show()



a.states()
a.plot('states',logy=True)
plt.tight_layout()
plt.show()

a.frequency()
print(a.freq_data)
a.plot('freq',logy=True, top=10)
plt.tight_layout()
plt.show()

a.weekly()
print(a.weekly_data)
a.plot('weekly',logy=True)
plt.tight_layout()
plt.show()

a.monthly()
print(a.monthly_data)
a.plot('monthly',logy=True)
plt.tight_layout()
plt.show()

y.lineages()
print(y.lineages_data)
y.plot('lineages', logy=True)
plt.tight_layout()
plt.show()

y.trends()
print(y.trends_data)
y.plot('trends', logy=True)
plt.tight_layout()
plt.show()


