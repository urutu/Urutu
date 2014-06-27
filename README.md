[Urutu](http://urutu.github.io)
=======

A Python based parallel programming library for GPUs

About
-----

Urutu integrates CUDA and OpenCL into a single code. That is, write a single code in Python run it using CUDA or OpenCL or both. It is portable to different hardware and operating systems.

System Requirements
-------------------

  -  Windows, Ubuntu (tested), Mac
  -  Python 2.7, GCC 4.6
  -  A GPU compatible with OpenCL or CUDA 5.0
  -  [PyOpenCL](http://mathema.tician.de/software/pyopencl) or [PyCUDA](http://mathema.tician.de/software/pycuda) installed


Setup
------

```shell
$ git clone https://github.com/urutu/Urutu.git
$ cd Urutu
$ sudo python2 setup.py install
```
For installing with Python 3, install PyCUDA and PyOpenCL with Python 3. Then, clone this repository and use
```shell
$ git clone https://github.com/urutu/Urutu.git
$ 2to3 -w Urutu
$ cd Urutu
$ sudo python3 setup.py install
```
=======

Sample Code
-----------

```python
from Urutu import *
import numpy as np

@Urutu("CL")
def divmul(a, b, c, d):
	__global is x, y
	x = a[0:100]
	y = b[0:100]
	t, u, v, w = 10, 10.0, 'opencl', "open.cl"
	c[tx] = x[tx] / y[tx]
	d[tx] = x[tx] * y[tx]
	return c, d

@Urutu("CU")
def addsub(a, b, e, f):
	__shared is x , y
	x = a[0:100]
	y = b[0:100]
	t, u, v, w = 11, 11.0, 'cuda', "cu.da"
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
print "Running on OpenCL.. \n", divmul([100,1,1], [1,1,1], a, b, c, d)
print "Running on CUDA.. \n", addsub([100,1,1], [1,1,1], a, b, e, f)
```
