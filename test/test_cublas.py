from Urutu import *
import numpy as np

@Urutu("gpu")
def Blas(_x,_y):
	Urmod.cublas.cublasSaxpy(h, _x.size, 1, _x, 2, _y, 2)
	return _y

a = np.random.randint(10,size=100)
b = np.random.randint(10,size=100)
print a,b,Blas([100,1,1],a,b)
