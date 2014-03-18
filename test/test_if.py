from Urutu import *
import numpy as np

@Urutu("CL")
def divmul(a, b, c, d):
	if tx > 50:
		c[tx] = a[tx] / b[tx]
	else:
		d[tx] = a[tx] * b[tx]
	return c, d

@Urutu("CU")
def addsub(a, b, e, f):
	if tx > 50 :
		f[tx] = a[tx] - b[tx]
	else:
		e[tx] = a[tx] + b[tx]
	return e, f

a = np.random.randint(10, size = 100)
b = np.random.randint(10, size = 100)
c = np.array(a, dtype = 'f')
d = np.empty_like(a)
e = np.empty_like(a)
f = np.empty_like(a)

print "The Array A is: \n",a
print "The Array B is: \n",b
print "Running on OpenCL.. \n",divmul([100,1,1], a, b, c, d)
print "Running on CUDA.. \n",addsub([100,1,1], a, b, e, f)
