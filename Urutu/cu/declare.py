## CUDA declare new arrays
## Created by: Aditya Atluri
## Date: Mar 03 2014

def decglobal(stmt, type_vars, var_nam, args, kernel):
#	print "In statement", stmt
	index = stmt.index('=') + 1
	deftype = type_vars[var_nam.index(stmt[index])]
#	print deftype
	if stmt.count(':') == 1:
		endindex = int(stmt[stmt.index(':') + 1])
		startindex = int(stmt[stmt.index(':') - 1])
		arraysize = int(endindex) - int(startindex)
	else:
		arraysize = args[var_nam.index(stmt[index])].size
		endindex = arraysize - 1
		startindex = 0
	kernel = "__device__ " + str(deftype[:-1]) + " " + str(stmt[0]) + "[" + str(arraysize) + "];\n" + kernel + str(stmt[0]) + "[tx] = " + str(stmt[index]) + "[tx + " + str(startindex) + "];\n"
	var_nam.append(stmt[index - 1])
	type_vars.append(str(deftype[:-1])+"*")
	return kernel, var_nam, type_vars

def decconstant(stmt, type_vars, var_nam, args, kernel):
	return
	print "In statement", stmt
	index = stmt.index('=') + 1
	deftype = type_vars[var_nam.index(stmt[index])]
#	print deftype
	if stmt.count(':') == 1:
		endindex = int(stmt[stmt.index(':') + 1])
		startindex = int(stmt[stmt.index(':') - 1])
		arraysize = int(endindex) - int(startindex)
	else:
		arraysize = args[var_nam.index(stmt[index])].size
		endindex = arraysize - 1
		startindex = 0
	kernel = kernel + "__constant__ " + str(deftype[:-1]) + " " + str(stmt[0]) + "[" + str(arraysize) + "];\n" + str(stmt[0]) + "[tx] = " + str(stmt[index]) + "[tx + " + str(startindex) + "];\n"
	var_nam.append(stmt[index - 1])
	type_vars.append(str(deftype[:-1])+"*")
	return kernel, var_nam, type_vars

def decshared(stmt, type_vars, var_nam, args, kernel):
#	print "In statement", stmt
	index = stmt.index('=') + 1
	deftype = type_vars[var_nam.index(stmt[index])]
#	print deftype
	if stmt.count(':') == 1:
		endindex = int(stmt[stmt.index(':') + 1])
		startindex = int(stmt[stmt.index(':') - 1])
		arraysize = int(endindex) - int(startindex)
	else:
		arraysize = args[var_nam.index(stmt[index])].size
		endindex = arraysize - 1
		startindex = 0
	kernel = kernel + "__shared__ " + str(deftype[:-1]) + " " + str(stmt[0]) + "[" + str(arraysize) + "];\n" + str(stmt[0]) + "[tx] = " + str(stmt[index]) + "[tx + " + str(startindex) + "];\n"
	var_nam.append(stmt[index - 2])
	type_vars.append(str(deftype[:-1])+"*")
	return kernel, var_nam, type_vars

def decregister(stmt, type_vars, var_nam, args, kernel):
	return
	print "In statement", stmt
	index = stmt.index('=') + 1
	deftype = type_vars[var_nam.index(stmt[index])]
#	print deftype
	if stmt.count(':') == 1:
		endindex = int(stmt[stmt.index(':') + 1])
		startindex = int(stmt[stmt.index(':') - 1])
		arraysize = int(endindex) - int(startindex)
	else:
		arraysize = args[var_nam.index(stmt[index])].size
		endindex = arraysize - 1
		startindex = 0
	kernel = kernel + "__register__ " + str(deftype[-1]) + " " + str(stmt[0]) + "[" + str(arraysize) + "];\n" + str(stmt[0]) + "[tx] = " + str(stmt[index]) + "[tx + " + str(startindex) + "];\n"
	var_nam.append(stmt[index - 1])
	type_vars.append(str(deftype[:-1])+"*")
	return kernel, var_nam, type_vars
