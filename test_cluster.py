import Cluster as c 



''' Unit test for this class ''' 
x = c.Cluster("from ca",verbose=True)
y = c.Cluster("x after 1/1/22",verbose=True)
z = c.Cluster("B.1.1.7 from ny before 10/1/22",verbose=True)
y.lineages()
print("y.lineages_data = "+y.lineages_data)
