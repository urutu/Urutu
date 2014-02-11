from Urutu import *
import numpy as np

@Urutu("CU")
def addsub(a,b,c,d):
	Tx, Ty, Tz = 100, 1, 1
	Bx, By, Bz = 1, 1, 1
	__global is x , y
	x = a[0:100]
	y = b[0:100]
	c[tx] = x[tx] + y[tx]
	d[tx] = x[tx] - y[tx]
	return c, d

a=np.random.randint(10,size=100)
b=np.random.randint(10,size=100)
c=np.empty_like(a)
d=np.empty_like(a)

print "The Array A is: \n",a
print "The Array B is: \n",b
print "Running on CUDA using Global Memory! \n",addsub(a,b,c,d)
