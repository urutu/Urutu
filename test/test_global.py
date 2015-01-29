from Urutu import *
import numpy as np

@Urutu("CL")
def divmul(a, b, c, d):
	__global is x , y
	x[tx] = a[tx]
	y[tx] = b[tx]
	c[tx] = x[tx] / y[tx]
	d[tx] = x[tx] * y[tx]
	return c, d

@Urutu("CU")
def addsub(a, b, e, f):
	__global is x , y
	x[tx] = a[tx]
	y[tx] = b[tx]
	e[tx] = x[tx] + y[tx]
	f[tx] = x[tx] - y[tx]
	return e, f

a = np.random.randint(10, size = 100)
b = np.random.randint(10, size = 100)
c = np.array(a, dtype = 'f')
d = np.empty_like(a)
e = np.empty_like(a)
f = np.empty_like(a)

print "The Array A is: \n", a
print "The Array B is: \n", b
print "Running on OpenCL.. \n", divmul(True,a, b, c, d)
print "Running on CUDA.. \n", addsub(True,a, b, e, f)
