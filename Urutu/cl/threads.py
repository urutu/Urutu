## OpenCL threads are initialized here!
## Created by: Aditya Atluri
## Date: Mar 03 2014

def tx(threads_dec,kernel):
	if threads_dec == False:
		string = "int tx = get_local_id(0);\n"
		kernel = kernel + string
		threads_dec = True
	return kernel, threads_dec

def ty(threads_dec,kernel):
	if threads_dec == False:
		string = "int ty = get_local_id(1);\n"
		kernel = kernel + string
		threads_dec = True
	return kernel, threads_dec

def tz(threads_dec, kernel):
	if threads_dec == False:
		string = "int tz = get_local_id(2);\n"
		kernel = kernel + string
		threads_dec = True
	return kernel, threads_dec

def threads_decl(stmt, var_nam, var_val, threads, type_vars):
	equ = stmt.index('=')
	kernel = ""
	if var_nam.count('Tx') < 1 and stmt.count('Tx') > 0:
		pos = stmt.index('Tx')
		var_nam.append(stmt[pos])
		kernel += "int Tx = get_local_size(0);\n"
		type_vars.append("int")
	if var_nam.count('Ty') < 1 and stmt.count('Ty') > 0:
		pos = stmt.index('Ty')
		var_nam.append(stmt[pos])
		kernel += "int Ty = get_local_size(1);\n"
		type_vars.append("int")
	if var_nam.count('Tz') < 1 and stmt.count('Tz') > 0:
		pos = stmt.index('Tz')
		var_nam.append(stmt[pos])
		kernel += "int Tz = get_local_size(2);\n"
		type_vars.append("int")
	return var_nam, var_val, threads, kernel, type_vars
