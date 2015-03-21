from Urutu import *
import numpy as np

@Urutu("gpu")
def solve(u, N, D2, it):
	nx, ny = N
	dx2, dy2 = D2
	x = i % nx
	y = i / nx
	if x == 0 or x == nx - 1 or y == 0 or y == ny-1:
		return 

