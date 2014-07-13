from Urutu import *
import numpy as np

@Urutu("CU")
def add(e,f,d,a,b,c):
	c[tx] = a[tx] + b[tx]
	d[tx] = a[tx] - b[tx]
	e[tx] = a[tx] * b[tx]
	f[tx] = a[tx] + b[tx]
	return c,d,e,f

a = np.random.randint(10,size=100)
b = np.random.randint(10,size=100)
c = np.empty_like(b)
d = np.empty_like(b)
e = np.empty_like(b)
f = np.empty_like(b)

print a,b,add([100,1,1],[1,1,1],e,f,d,a,b,c)
