
from Urutu import *
import numpy as np

@Urutu("gpu")
def fft(ax, ay, b_x, by, cx, cy, size):
	tid = tx + bx * Tx
	T = Tx
	B = Bx
	for i in range(tid,size,T*B):
		cx[i] = 2.0*(ax[i] * b_x[i] - ay[i] * by[i])
		cy[i] = 2.0*(ax[i] * by[i] + ay[i] * b_x[i])
	return cx, cy


def main():
	ax = np.random.randint(10, size = 10)
	ay = np.random.randint(10, size = 10)
	bx = np.random.randint(10, size = 10)
	by = np.random.randint(10, size = 10)
	cx = np.empty_like(ax)
	cy = np.empty_like(ay)
	size = 1000
	print fft([100,1,1],[1,1,1],ax,ay,bx,by,cx,cy,size)

if __name__ == '__main__':
	main()

