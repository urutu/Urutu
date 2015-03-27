
from Urutu import *
import numpy as np

@Urutu("gpu")
def fft(ax, ay, b_x, by, cx, cy):
	tid = tx + bx * Tx
	T = Tx
	B = Bx
	size = 1000
	for i in range(tid,size,T*B):
		cx[i] = 2.0*(ax[i] * b_x[i] - ay[i] * by[i])
		cy[i] = 2.0*(ax[i] * by[i] + ay[i] * b_x[i])
	return cx, cy


def main():
	ax = np.random.randint(10, size = 1000)
	ay = np.random.randint(10, size = 1000)
	bx = np.random.randint(10, size = 1000)
	by = np.random.randint(10, size = 1000)
	cx = np.empty_like(ax)
	cy = np.empty_like(ay)
	print fft([100,1,1],[1,1,1],ax,ay,bx,by,cx,cy)

if __name__ == '__main__':
	main()

