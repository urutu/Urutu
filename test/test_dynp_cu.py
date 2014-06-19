from Urutu import *
import numpy as np

@Urutu("CU")
def math(a, b, c, d, e, f):
	__shared is x , y
	x = a[0:100]
	y = b[0:100]

	def add(p,q):
		p = p + 1
		return p+q

	c[tx] = add(x[tx],y[tx])

	def sub(p,q,d):
		p[tx] = 2*p[tx]
		d[tx] = p[tx] - q[tx]

	def saxpy(s,a,p,b,q):
		s[tx] = a*p[tx] + b*q[tx]

	sub([100,1,1],[1,1,1],a,b,d)
	saxpy(f,1.0345,x,-2,y)
	return c, d, e, f

a = np.random.randint(10, size = 100)
b = np.random.randint(10, size = 100)
c = np.empty_like(a)
d = np.empty_like(a)
e = np.empty_like(a)
f = np.array(a, dtype = 'd')

print "The Array A is: \n", a
print "The Array B is: \n", b
print "Running on CUDA.. \n", math([100,1,1],[100,1,1],a, b, c, d, e, f)
