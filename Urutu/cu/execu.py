import pycuda.driver as cuda
import pycuda.autoinit
from pycuda.compiler import SourceModule
import numpy

class cu_exe:
	def exe_cu(self,stringg,func_name,threads,blocks,args,returns):
		cu_args = []
		for arg in args:
			cu_args.append(cuda.mem_alloc(args[0].nbytes))
		cuda.memcpy_htod(a_gpu,args[0])
		b_gpu=cuda.mem_alloc(args[1].nbytes)
		cuda.memcpy_htod(b_gpu,args[1])
		c_gpu=cuda.mem_alloc(args[2].nbytes)
		cuda.memcpy_htod(c_gpu,args[2])
		d=numpy.empty_like(args[0])
		d_gpu=cuda.mem_alloc(d.nbytes)
		mod=SourceModule(stringg)
		func=mod.get_function(func_name)
		func(a_gpu,b_gpu,c_gpu,d_gpu,block=(2*threads[0],2*threads[1],1),grid=(2*blocks[0],2*blocks[1],1))
		cuda.memcpy_dtoh(d,d_gpu)
		return d
