from Urutu import *
import numpy as np


@Urutu("gpu")
def black_scholes(si, xi, ti, d1, d2, call_result, put_result, sqrt_ti):
	A1 = 0.31938153
	A2 = -0.356563782
	A3 = 1.781477937
	A4 = -1.821255978
	A5 = 1.330274429
	RSQRT2PI = 0.39894228040
	R = 0.02
	V = 0.3
	tid = tx + bx * Tx
	sqrt_ti[tid] = sqrt(ti[tid])
	d1[tid] = (log(si[tid]/xi[tid]) + (R + 0.5 * V * V) * ti[tid]) / (V * sqrt_ti[tid])
	d2[tid] = d1[tid] - V * sqrt_ti[tid]
	K = 1.0 / (1.0 + 0.2316419 * abs(d1[tid])) 
	d1[tid] = RSQRT2PI * exp(-0.5 * d1[tid] * d1[tid]) * (K * (A1 + K * (A2 + K * (A3 + K*(A4+K*A5))))) 
	K = 1.0 / (1.0 + 0.2316419 * abs(d2[tid])) 
	d2[tid] = RSQRT2PI * exp(-0.5 * d2[tid] * d2[tid]) * (K * (A1 + K * (A2 + K * (A3 + K*(A4+K*A5))))) 
	put_result[tid] = exp(-R * ti[tid])
	call_result[tid] = si[tid] * d1[tid] - xi[tid] * put_result[tid] * d2[tid]
	put_result[tid] = xi[tid] * put_result[tid] * (1.0 - d2[tid]) - si[tid] * (1.0 - d1[tid])
	return call_result, put_result

def rand_floats(n, min, max):
	diff = np.float32(max) - np.float32(min)
	rands = np.array(np.random.random(n), dtype=np.float32)
	rands = rands * diff
	rands = rands + np.float32(min)
	return rands

def main():
	n = 100
	S = rand_floats(n, 5, 30)
	X = rand_floats(n, 1, 100)
	T = rand_floats(n, 0.25, 10)
	sqrt_ti = np.empty_like(X)
	call_result = np.empty_like(X)
	put_result = np.empty_like(X)
	d1 = np.empty_like(X)
	d2 = np.empty_like(X)
	print black_scholes([100,1,1],[30,1,1],S, X, T, d1, d2, call_result, put_result, sqrt_ti)
#	print black_scholes(True,S, X, T, d1, d2, call_result, put_result, sqrt_ti)

if __name__ == '__main__':
	main()
