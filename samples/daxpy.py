from Urutu import *
import numpy as np

@Urutu("gpu")
def daxpy(d,a,x,b,y):
	tid = tx + bx * Tx
	d[tid] = a*x[tid] + b*y[tid]
	return d

def main():
	N = 10000
	x = np.random.randint(10, size = N)
	y = np.random.randint(10, size = N)
	d = np.empty_like(x)
	a, b = 1.0, 2.0
	print daxpy([500,1,1],[N/500,1,1],d,a,x,b,y)

if __name__ == '__main__':
	main()
