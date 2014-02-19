from Urutu import *
import numpy as np

@Urutu("CL")
def divmul(a,b,c,d):
	Tx, Ty, Tz = 100, 1, 1
	Bx, By, Bz = 1, 1, 1
	__global is x , y
	x = a[0:100]
	y = b[0:100]
	c[tx] = x[tx] / y[tx]
	d[tx] = x[tx] * y[tx]
	return c, d

@Urutu("CU")
def addsub(a,b,e,f):
	Tx, Ty, Tz = 100, 1, 1
	Bx, By, Bz = 1, 1, 1
	__global is x , y
	x = a[0:100]
	y = b[0:100]
	e[tx] = x[tx] + y[tx]
	f[tx] = x[tx] - y[tx]
	return e, f

a=np.random.randint(10,size=100)
b=np.random.randint(10,size=100)
c=np.array(a,dtype='f')
d=np.empty_like(a)
e=np.empty_like(a)
f=np.empty_like(a)

print "The Array A is: \n",a
print "The Array B is: \n",b
print "Running on OpenCL.. \n",divmul(a,b,c,d)
print "Running on CUDA.. \n",addsub(a,b,e,f)
