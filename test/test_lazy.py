from Urutu import *
import numpy as np

@Urutu("gpu")
def math(a, b, c, d, e, f):
	__shared is x , y
	x[tx] = a[tx]
	y[tx] = b[tx]

	c[tx] = x[tx] + y[tx] + 1

	d[tx] = 2*x[tx] - y[tx]

	f[tx] = 1.0345*x[tx] - 2*y[tx]

	return c, d, e, f

a = np.random.randint(10, size = 100)
b = np.random.randint(10, size = 100)
c = np.empty_like(a)
d = np.empty_like(a)
e = np.empty_like(a)
f = np.array(a, dtype = 'd')

print "The Array A is: \n", a
print "The Array B is: \n", b
#print "", math(True, a,b,c,d,e,f)
print "Running on GPU.. \n", math([100,1,1],[1,1,1],a, b, c, d, e, f)
