from Urutu import *
import numpy as np

@Urutu("gpu")
def divmul(a, b, c, d):
	c[tx+blockDim.x*bx] = a[tx+blockDim.x*bx] / b[tx+blockDim.x*bx]
	d[tx+blockDim.x*bx] = a[tx+blockDim.x*bx] * b[tx+blockDim.x*bx]
	return c, d

a = np.random.randint(10, size = 100)
b = np.random.randint(10, size = 100)
c = np.array(a, dtype = 'f')
d = np.empty_like(a)

print "The Array A is: \n",a
print "The Array B is: \n",b
print "Running on CUDA.. \n",divmul([50,1,1],[2,1,1],a, b, c, d)
