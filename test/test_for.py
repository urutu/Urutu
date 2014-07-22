from Urutu import *
import numpy as np

@Urutu("CU")
def add(s,x,y):
	for j in range(10):
		s[tx+10*j] = x[tx+10*j] + y[tx+10*j]
	return s

x = np.random.randint(10, size = 100)
y = np.random.randint(10, size = 100)
s = np.empty_like(x)

print "The Array A is: \n",x
print "The Array B is: \n",y
print "Running on CUDA.. \n",add([10,1,1],[1,1,1],s,x,y)
# for i in a:

# for i in range(len(a),10,len(b)):
