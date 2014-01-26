import pycuda.driver as cuda
import pycuda.autoinit
from pycuda.compiler import SourceModule
import numpy

class cu_exe:
	cu_args = []
	args = []
	argl = 0
	retl = 0
	def exe_cu(self,stringg,func_name,threads,blocks,args,returns):
		self.args = args
		self.argl = len(args)
		self.retl = len(returns)
		self.allocargs()
		self.htod()
		mod=SourceModule(stringg)
		func=mod.get_function(func_name)
		if self.argl == 1:
			func(self.cu_args[0],block=(threads[0],threads[1],threads[2]),grid=(blocks[0],blocks[1],blocks[2]))
		elif self.argl == 2:
			func(self.cu_args[0],self.cu_args[1],block=(threads[0],threads[1],threads[2]),grid=(blocks[0],blocks[1],blocks[2]))
		elif self.argl == 3:
			func(self.cu_args[0],self.cu_args[1],self.cu_args[2],block=(threads[0],threads[1],threads[2]),grid=(blocks[0],blocks[1],blocks[2]))
		elif self.argl == 4:
			func(self.cu_args[0],self.cu_args[1],self.cu_args[2],self.cu_args[3],block=(threads[0],threads[1],threads[2]),grid=(blocks[0],blocks[1],blocks[2]))
		elif self.argl == 5:
			func(self.cu_args[0],self.cu_args[1],self.cu_args[2],self.cu_args[3],self.cu_args[4],block=(threads[0],threads[1],threads[2]),grid=(blocks[0],blocks[1],blocks[2]))
		elif self.argl == 6:
			func(self.cu_args[0],self.cu_args[1],self.cu_args[2],self.cu_args[3],self.cu_args[4],self.cu_args[5],block=(threads[0],threads[1],threads[2]),grid=(blocks[0],blocks[1],blocks[2]))
		elif self.argl == 7:
			func(self.cu_args[0],self.cu_args[1],self.cu_args[2],self.cu_args[3],self.cu_args[4],self.cu_args[5],self.cu_args[6],block=(threads[0],threads[1],threads[2]),grid=(blocks[0],blocks[1],blocks[2]))
		elif self.argl == 8:
			func(self.cu_args[0],self.cu_args[1],self.cu_args[2],self.cu_args[3],self.cu_args[4],self.cu_args[5],self.cu_args[6],self.cu_args[7],block=(threads[0],threads[1],threads[2]),grid=(blocks[0],blocks[1],blocks[2]))
		elif self.argl == 9:
			func(self.cu_args[0],self.cu_args[1],self.cu_args[2],self.cu_args[3],self.cu_args[4],self.cu_args[5],self.cu_args[6],self.cu_args[7],self.cu_args[8],block=(threads[0],threads[1],threads[2]),grid=(blocks[0],blocks[1],blocks[2]))
		elif self.argl == 10:
			func(self.cu_args[0],self.cu_args[1],self.cu_args[2],self.cu_args[3],self.cu_args[4],self.cu_args[5],self.cu_args[6],self.cu_args[7],self.cu_args[8],self.cu_args[9],block=(threads[0],threads[1],threads[2]),grid=(blocks[0],blocks[1],blocks[2]))
		self.dtoh()
		if self.retl == 0:
			return
		elif self.retl == 1:
			return self.args[self.argl - self.retl]
		elif self.retl == 2:
			return self.args[self.argl - self.retl], self.args[self.argl - self.retl + 1]
		elif self.retl == 3:
			return self.args[self.argl - self.retl], self.args[self.argl - self.retl + 1], self.args[self.argl - self.retl + 2]
		elif self.retl == 4:
			return self.args[self.argl - self.retl], self.args[self.argl - self.retl + 1], self.args[self.argl - self.retl + 2], self.args[self.argl - self.retl + 3]

	def allocargs(self):
		for arg in self.args:
			self.cu_args.append(cuda.mem_alloc(arg.nbytes))

	def htod(self):
		for i in range(self.argl-self.retl):
			cuda.memcpy_htod(self.cu_args[i],self.args[i])

	def dtoh(self):
		for i in range(self.retl):
			cuda.memcpy_dtoh(self.args[self.argl-self.retl+i],self.cu_args[self.argl-self.retl+i])
