## OpenCL threads are initialized here!
## Created by: Aditya Atluri
## Date: Mar 03 2014

def tx(threads_dec,kernel):
	if threads_dec == False:
		string = "int tx = get_global_id(0);\n"
		kernel = kernel + string
		threads_dec = True
	return kernel, threads_dec

def ty(threads_dec,kernel):
	if threads_dec == False:
		string = "int ty = get_global_id(1);\n"
		kernel = kernel + string
		threads_dec = True
	return kernel, threads_dec

def tz(threads_dec, kernel):
	if threads_dec == False:
		string = "int tz = get_global_id(2);\n"
		kernel = kernel + string
		threads_dec = True
	return kernel, threads_dec

def threads_decl(stmt, var_nam, var_val, threads):
	equ = stmt.index('=')
	if var_nam.count('Tx') < 1 and stmt.count('Tx') == 1:
		pos = stmt.index('Tx')
		pos_val = stmt[pos + 1 + equ]
		var_nam.append(stmt[pos])
		var_val.append(int(pos_val))
		threads[0] = int(pos_val)
	if var_nam.count('Ty') < 1 and stmt.count('Ty') == 1:
		pos = stmt.index('Ty')
		pos_val = stmt[pos + 1 + equ]
		var_nam.append(stmt[pos])
		var_val.append(int(pos_val))
		threads[1] = int(pos_val)
	if var_nam.count('Tz') < 1 and stmt.count('Tz') == 1:
		pos = stmt.index('Tz')
		pos_val = stmt[pos + 1 + equ]
		var_nam.append(stmt[pos])
		var_val.append(int(pos_val))
		threads[2] = int(pos_val)
	return var_nam, var_val, threads
