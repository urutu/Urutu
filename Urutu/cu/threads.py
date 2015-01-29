## CUDA threads are initialized here!
## Created by: Aditya Atluri
## Date: Mar 03 2014

def tx(threads_dec,kernel):
	if threads_dec == False:
		string = "int tx = threadIdx.x;\n"
		kernel = kernel + string
		threads_dec = True
	return kernel, threads_dec

def ty(threads_dec,kernel):
	if threads_dec == False:
		string = "int ty = threadIdx.y;\n"
		kernel = kernel + string
		threads_dec = True
	return kernel, threads_dec

def tz(threads_dec, kernel):
	if threads_dec == False:
		string = "int tz = threadIdx.z;\n"
		kernel = kernel + string
		threads_dec = True
	return kernel, threads_dec

def threads_decl(stmt, var_nam, var_val, threads, type_vars):
	equ = stmt.index('=')
	kernel = ""
	if var_nam.count('Tx') < 1 and stmt.count('Tx') > 0:
		pos = stmt.index('Tx')
		var_nam.append(stmt[pos])
		kernel += "int Tx = blockDim.x;\n"
		type_vars.append("int")
	if var_nam.count('Ty') < 1 and stmt.count('Ty') > 0:
		pos = stmt.index('Ty')
		var_nam.append(stmt[pos])
		kernel += "int Ty = blockDim.y;\n"
		type_vars.append("int")
	if var_nam.count('Tz') < 1 and stmt.count('Tz') > 0:
		pos = stmt.index('Tz')
		var_nam.append(stmt[pos])
		kernel += "int Tz = blockDim.z;\n"
		type_vars.append("int")
	return var_nam, var_val, threads, kernel, type_vars

