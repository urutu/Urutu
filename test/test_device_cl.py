from Urutu import *
import numpy as np

@Urutu("CL")
def math(a, b, c):
	__shared is x , y
	x = a[0:100]
	y = b[0:100]
	def add(p,q):
		p = p + 1
		return p+q
	c[tx] = add(x[tx],y[tx])
	return c

a = np.random.randint(10, size = 100)
b = np.random.randint(10, size = 100)
c = np.empty_like(a)

print "The Array A is: \n", a
print "The Array B is: \n", b
print "Running on OpenCL.. \n", math([100,1,1],[100,1,1],a, b, c)
