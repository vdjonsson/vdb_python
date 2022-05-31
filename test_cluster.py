import Cluster as c 
import matplotlib.pyplot as plt
import Pattern as pat 

''' Unit test for this class ''' 
x = c.Cluster("from ca",cluster_name ='x',verbose=True)
y = c.Cluster("x after 12/1/20",verbose=True)
z = c.Cluster("B.1.1.7 from ny before 10/1/22",verbose=True)


''' Define cluster a '''
a = c.Cluster('from France + Japan', verbose=True)

''' Find subcluster with a particular mutation pattern '''
ca = a.containing('E484K N501Y') # OR ca = a.containing(['E484K', 'N501Y'])

p1 = pat.Pattern('E484K N501Y')
nca = a.notcontaining(p1)

''' Print out information for cluster a '''
a.info()

''' Recreate a different cluster a ''' 
a = c.Cluster('from Germany', verbose=True)
a.info()

a.countries()
print(a.countries_data)
a.plot('countries',logy=True)


frequency_data = a.frequency(plot=True, plot_args={'logy':True, 'top':15, 'save':True})

nca = a.notcontaining('E484K N501Y') # OR nca = a.notcontaining(['E484K', 'N501Y'])
print(nca)
nca.info()

ca.frequency()
print(ca.freq_data) 
ca.plot('freq',logy=True, top=10)

s = z.lineage('B.1.1')
z.info() 

trends_data = z.trends(plot=True)

s = z.sample(0.38)
s.trends()
s.info()

s.frequency()
s.plot('freq',logy=True, top=10)

aa = a.range('6/1/2020-8/1/2020') # OR
s = a.range(['6/1/2020','8/1/2020'])

o = a.after('4/1/2022')
o.frequency(plot=True, plot_args={'logy':True, 'top':10})

a.states()
a.plot('states',logy=True)

a.frequency()
print(a.freq_data)
a.plot('freq',top=10)


a.weekly()
print(a.weekly_data)
a.plot('weekly')


a.monthly()
print(a.monthly_data)
a.plot('monthly')

lin1 = y.lineages(plot=True, plot_args={'logy':True})
print(lin1) 

y.trends()
print(y.trends_data)
y.plot('trends')

