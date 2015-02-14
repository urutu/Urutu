from Urutu import *
import numpy as np

def average(c):
	d = 0
	for i in c:
		d+=i
	return d


def f():
	sum = 0
	print sum + 1


# Only args can be sent to and fro from CPU function
@Urutu("gpu")
def mul(a, b, c, d, e, f):
	c[tx] = a[tx] + b[tx]
	d[0] = cpu.average(c)
	e[0] = cpu.average(b)
	f[tx] = e[0] * c[tx]
	return d,e,f

a = np.ones(100)
b = np.ones(100)
c = np.empty_like(a)
d = np.ones(1)
e = np.empty_like(d)
f = np.empty_like(a)

print a, b, mul([100,1,1],[1,1,1],a,b,c,d,e,f)
