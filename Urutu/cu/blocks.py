## CUDA blocks are initialized here!
## Created by: Aditya Atluri
## Date: Mar 03 2014

def bx(blocks_dec, kernel):
	if blocks_dec == False:
		string = "int bx = blockIdx.x;\n"
		kernel = kernel + string
		blocks_dec = True
	return kernel, blocks_dec

def by(blocks_dec, kernel):
	if blocks_dec == False:
		string = "int by = blockIdx.y;\n"
		kernel = kernel + string
		blocks_dec = True
	return kernel, blocks_dec

def bz(blocks_dec, kernel):
	if blocks_dec == False:
		string = "int bz = blockIdx.z;\n"
		kernel = kernel + string
		blocks_dec = True
	return kernel, blocks_dec

def blocks_decl(stmt, var_nam, var_val, blocks, type_vars):
	equ = stmt.index('=')
	kernel = ""
	if var_nam.count('Bx') < 1 and stmt.count('Bx') > 0:
		pos = stmt.index('Bx')
		var_nam.append(stmt[pos])
		kernel += "int Bx = gridDim.x;\n"
		type_vars.append("int")
	if var_nam.count('By') < 1 and stmt.count('By') > 0:
		pos = stmt.index('By')
		var_nam.append(stmt[pos])
		kernel += "int By = gridDim.y;\n"
		type_vars.append("int")
	if var_nam.count('Bz') < 1 and stmt.count('Bz') > 0:
		pos = stmt.index('Bz')
		var_nam.append(stmt[pos])
		kernel += "int Bz = gridDim.z;\n"
		type_vars.append("int")
	return var_nam, var_val, blocks, kernel, type_vars
