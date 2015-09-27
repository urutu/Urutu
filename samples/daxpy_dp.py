from Urutu import *
import numpy as np

@Urutu("gpu")
def daxpy(d,a,x,b,y):
	d = a*x + b*y
	return d

def main():
	N = 10000
	x = np.random.randint(10, size = N)
	y = np.random.randint(10, size = N)
	d = np.empty_like(x)
	a, b = 1.0, 2.0
	print daxpy(d,a,x,b,y)
	if a*x[0] + b*y[0] == d[0]:
		print "Success"

if __name__ == '__main__':
	main()
