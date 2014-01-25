[Urutu](http://urutu.github.io)
=====

A GPU based parallel programming library for Python

System Requirements
-------------------

	-	Windows, Ubuntu (tested), Mac
	-	Python 2.7, GCC 4.6
	-	A GPU compatible with OpenCL or CUDA 5.0
	-	[PyOpenCL](http://mathema.tician.de/software/pyopencl) installed
		or
	-	[PyCUDA](http://mathema.tician.de/software/pycuda) installed

```python
from Urutu import *
import numpy as np

@Urutu("CL")
def mul(a,b,c,d):
	tx, ty, tz = 100, 1, 1
	bx, by, bz = 1, 1, 1
	c[tx] = a[tx] * b[tx]
	d[tx] = a[tx] + b[tx]
	return c, d

a=np.random.randint(10,size=100)
b=np.random.randint(10,size=100)
c=np.random.randint(10,size=100)
d=np.random.randint(10,size=100)

print a,b
print mul(a,b,c,d)
```
