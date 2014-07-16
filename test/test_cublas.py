from Urutu import *
import numpy as np

@Urutu("gpu")
def Blas(x,y):
	x[tx] += 1
	Urmod.cublas.cublasSaxpy(h, x.size, 1, x.gpudata, 1, y.gpudata, 1)
	return x

a = np.random.rand(100).astype(np.float32)
b = np.random.rand(100).astype(np.float32)
print Blas([100,1,1],a,b)
