from Urutu import *
import numpy as np

@Urutu("gpu")
def CSR(ptr,indices,data,x,y):
	num_rows = 512
	row = tx + bx * Tx
	if row < num_rows:
		dot = 0.0
		num_start = ptr[row]
		num_end = ptr[row+1]
		for n in range(num_end-num_start):
			j = n + num_start
			dot += data[j] * x[indices[j]]
		y[row] += dot
	return y

def main():
        num_rows,num_cols,num_cols_per_row = 512,512,512
        data = np.random.randint(10,size=num_rows*num_cols)
        x = np.random.randint(10,size=num_rows*num_cols)
        ind_ = np.random.randint(num_cols,size=num_rows*num_cols)
        ind = np.array(ind_,dtype=np.int32)
	ptr_ = np.random.randint(num_cols,size=num_rows*num_cols)
	ptr = np.array(ptr_,dtype=np.int32)
        y = np.empty_like(x)
        CSR([num_cols,1,1],[num_rows,1,1],ptr,ind,data,x,y)

if __name__ == '__main__':
        main()

