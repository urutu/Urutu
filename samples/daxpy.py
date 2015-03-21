from Urutu import *
import numpy as np

@Urutu("gpu")
def daxpy(d,x,y):
	tid = tx + bx * Tx
	d[tid] = 1.0*x[tid] + 2.0*y[tid]
	return d

def main():
	N = 10000
	x = np.random.randint(N)
	y = np.random.randint(N)
	d = np.empty_like(x)
	print daxpy([500,1,1],[N/500,1,1],d,x,y)

if __name__ == '__main__':
	main()
