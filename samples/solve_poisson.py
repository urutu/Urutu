'''

'''

from Urutu import *
import numpy as np

@Urutu("gpu")
def poisson(Cx, Cy, a, kx, ky):
	idx = tx + bx * Bx
	idy = ty + by * By
	N = 10
	if idx < N and idy < N:
		index = idx + idy * N
		scale = kx[idx]*kx[idx] + ky[idy]*ky[idy]
		if idx == 0 and idy == 0:
			scale = -1.0
		scale = -1.0/scale
		Cx[index] = a[index] * scale
		Cy[index] = 0.0 * scale
	return Cx, Cy

def main():
	kx = np.random.randint(10,size=10)
	ky = np.random.randint(10,size=10)
	a = np.random.randint(10,size=10)
	Cx = np.empty_like(kx)
	Cy = np.empty_like(ky)
	print poisson([10,1,1],[1,1,1],Cx, Cy, a, kx, ky)

if __name__ == '__main__':
	main()
