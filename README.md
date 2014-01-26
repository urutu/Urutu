[Urutu](http://urutu.github.io)
=======

A GPU based parallel programming library for Python

System Requirements
-------------------

  -  Windows, Ubuntu (tested), Mac
  -  Python 2.7, GCC 4.6
  -  A GPU compatible with OpenCL or CUDA 5.0
  -  [PyOpenCL](http://mathema.tician.de/software/pyopencl) or [PyCUDA](http://mathema.tician.de/software/pycuda) installed

Sample Code
-----------

```python
from Urutu import *
import numpy as np

@Urutu("CL")
def divmul(a,b,c,d):
	Tx, Ty, Tz = 100, 1, 1
	Bx, By, Bz = 1, 1, 1
	c[tx] = a[tx] / b[tx]
	d[tx] = a[tx] * b[tx]
	return c, d

@Urutu("CU")
def addsub(a,b,e,f):
	Tx, Ty, Tz = 100, 1, 1
	Bx, By, Bz = 1, 1, 1
	e[tx] = a[tx] + b[tx]
	f[tx] = a[tx] - b[tx]
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
```
