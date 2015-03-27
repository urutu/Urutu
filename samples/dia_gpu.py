from Urutu import *
import numpy as np

@Urutu("gpu")
def DIA(offsets,data,x,y):
	num_cols, num_diags, num_rows = 512,512,512
	row = tx + bx * Tx
	if row < num_rows:
		dot = 0.0
		for n in range(num_diags):
			col = row + offsets[n]
			val = data[num_rows * n + row]
			if col >= 0 and col < num_cols:
				dot += val * x[col]
		y[row] += dot
	return y

def main():
        num_rows,num_cols,num_cols_per_row = 512,512,512
        data = np.random.randint(10,size=num_rows*num_cols)
        x = np.random.randint(10,size=num_rows*num_cols)
        ind_ = np.random.randint(num_cols,size=num_rows*num_cols)
        ind = np.array(ind_,dtype=np.int32)
        y = np.empty_like(x)
        y = DIA([num_rows,1,1],[num_cols,1,1],ind,data,x,y)

if __name__ == '__main__':
        main()


