def create_string(string_args):
	code = ""
	for i in string_args:
		if i is string_args[0]:
			code += i
		else:
			code += ", " + i
	return code + ")\n"

def ur_cublas(function,string_args,args):
	try:
		import scikits.cuda.cublas as cublas
		import numpy as np
	except:
		return
	code = string_args[0]+" = cublas.cublasCreate()\ncublas."
	code_end = "cublas.cublasDestroy("+ string_args[0] + ")\n"
	if function == "cublasIsamax":
		if len(string_args) == 4:
			code += "cublasIsamax( " + create_string(string_args)
	if function == "cublasSaxpy":
		if len(string_args) == 7:
			code += "cublasSaxpy( " + create_string(string_args)
	code += code_end
	exec code
	return

def execute(module,function,string_args,cu_args):
	if module == "cublas":
		return ur_cublas(function,string_args,cu_args)
