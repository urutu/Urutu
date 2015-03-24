from Urutu import *
import numpy as np
import time

@Urutu("gpu")
def count(a, b):
	n = 1000
	tid = tx + bx * Tx
	for i in range(n):
		if a[i+tid*n] > 1:
			b[tid] += 10
	for j in range(n):
		b[0] += b[j]
	return b


def main():
	N = 1000000
	a = np.random.randint(12,size = N)
	b = np.empty_like(a)
	start = time.time()
	print count([1,1,1],[1000,1,1],a,b)
	print b[0]

if __name__ == '__main__':
	main()
