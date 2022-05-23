import Cluster as c 
import matplotlib.pyplot as plt


''' Unit test for this class ''' 
x = c.Cluster("from ca",verbose=True)
y = c.Cluster("x after 12/1/20",verbose=True)
z = c.Cluster("B.1.1.7 from ny before 10/1/22",verbose=True)
a = c.Cluster('from France + Japan', verbose=True)


a.countries()
print(a.countries_data)
a.plot('countries',logy=True)
plt.tight_layout()
plt.show()

a.states()
print(a.states_data)
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


