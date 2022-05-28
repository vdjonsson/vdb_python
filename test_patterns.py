from setup import *
a = cl("ca")
b = cl("fl")
c = a + b
d = b.after("2/1/21")
cl("ca")
v("clusters")
cl("fl").info()
x = cl("us").states()
v("clusters")
x
z=cl("from ca after 2/1/22")
world = cl("world")
world.info()
world.after("2/1/21")
x = cl("alpha")
xx = x.consensus()
xx
xx.info()
y = cl("beta")
yy = y.consensus()
zz = xx & yy
zz.info()
v("zz")
zz.data
yy.info()
print(yy)
world.containing(yy)
world.notcontaining(yy)
p1 = Cluster.pat.Pattern("E484K N501Y")
p2 = d.patterns()
p3 = d.consensus()
v("diff p2 p3")
p2.info()
x.info()
p2.count
qqq = "ma"
qqq = cl("ma")
world.count
v("clusters")
qqq.info()
v("diff p2 p3")
v("diff b c")
diff(b,c)
v("diff b c")
c == b
v("c == b")
c != b
v("patterns")
xx == yy
