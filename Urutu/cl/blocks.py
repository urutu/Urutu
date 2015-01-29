## OpenCL blocks are initialized here!
## Created by: Aditya Atluri
## Date: Mar 03 2014

def bx(blocks_dec, kernel):
	if blocks_dec == False:
		string = "int bx = (get_global_id(0) - get_local_id(0)) / get_local_size(0);\n"
		kernel = kernel + string
		blocks_dec = True
	return kernel, blocks_dec

def by(blocks_dec, kernel):
	if blocks_dec == False:
		string = "int by = (get_global_id(1) - get_local_id(1)) / get_local_size(1);\n"
		kernel = kernel + string
		blocks_dec = True
	return kernel, blocks_dec

def bz(blocks_dec, kernel):
	if blocks_dec == False:
		string = "int bz = (get_global_id(2) - get_local_id(2)) / get_local_size(2);\n"
		kernel = kernel + string
		blocks_dec = True
	return kernel, blocks_dec

def blocks_decl(stmt, var_nam, var_val, blocks):
	equ = stmt.index('=')
	if var_nam.count('Bx') < 1:
		pos = stmt.index('Bx')
		pos_val = stmt[pos + 1 + equ]
		var_nam.append(stmt[pos])
		var_val.append(int(pos_val))
		blocks[0] = int(pos_val)
	if var_nam.count('By') < 1:
		pos = stmt.index('By')
		pos_val = stmt[pos + 1 + equ]
		var_nam.append(stmt[pos])
		var_val.append(int(pos_val))
		blocks[1] = int(pos_val)
	if var_nam.count('Bz') < 1:
		pos = stmt.index('Bz')
		pos_val = stmt[pos + 1 + equ]
		var_nam.append(stmt[pos])
		var_val.append(int(pos_val))
		blocks[2] = int(pos_val)
	return var_nam, var_val, blocks
