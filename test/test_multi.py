from Urutu import *
import numpy as np

@Urutu("gpu")
def add(a, b, c):
	c[tx] = a[tx] + b[tx]
	return c

@Urutu("gpu")
def sub(a, b, d):
	d[tx] = a[tx] + b[tx]
	return d

@Urutu("gpu")
def math(a, b, c, d):
	sub(a, b, d)
	c = add(a, b, c)
	return c, d

a = np.random.randint(10, size=100)
b = np.random.randint(10, size=100)
c = np.empty_like(a)
d = np.empty_like(a)

threads = [100,1,1]
blocks = [1,1,1]

print math(True,a,b,c,d)
print "On GPU:", math(threads,blocks,a,b,c,d)

