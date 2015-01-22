import numpy

def exe_map(code_map, name_map, args_map, lengths_map):
	try:
		import pycuda.driver as cuda
		import pycuda.autoinit
		from pycuda.compiler import SourceModule
	except:
		return
	mod=SourceModule(code_map)

# ismap[] = True, mapcode[], mapname[], mapargs[]
