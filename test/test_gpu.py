from Urutu import *
import numpy as np

@Urutu("gpu")
def math(a, b, c, d, e, f):
	__shared is x , y
	x = a[0:100]
	y = b[0:100]

	def add(p,q):
		p = p + 1
		return p+q

	c[tx] = add(x[tx],y[tx])

	def sub(p,q):
		p[tx] = 2*p[tx]
		return p[tx] - q[tx]

	def saxpy(s,a,p,b,q):
		s[tx] = a*p[tx] + b*q[tx]

	d[tx] = sub(x,y)
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
print "Running on GPU.. \n", math([100,1,1],[100,1,1],a, b, c, d, e, f)
