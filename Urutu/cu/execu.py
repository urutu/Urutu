# Developed by Aditya Atluri
# Date: 18 Jan 2014
# Mail: pyurutu@gmail.com
# This file contains the execution of CUDA code using PyCUDA
# Modified: 18 Jan 2014

import numpy

class cu_exe:
	cu_args = []
	args = []
	argl = 0
	retl = 0
	returns = []
	nam_returns = []
	nam_args = []
	id_ret = []
	is_alloc = []
	def exe_cu(self,stringg,func_name,threads,blocks,dyn_p,is_shared):
		try:
			import pycuda.driver as cuda
			import pycuda.autoinit
			from pycuda.compiler import SourceModule
		except:
			return
		if dyn_p is True:
			mod=SourceModule(stringg, options=['-rdc=true'],linkers=['-lcudadevrt'])
		else:
			mod=SourceModule(stringg)
		func=mod.get_function(func_name)
		shared_mem = 0
		if is_shared == True:
			for i in self.args:
				if shared_mem < i.size:
					shared_mem = i.size
		if is_shared == True:
			func(*self.cu_args,block=(threads[0],threads[1],threads[2]),grid=(blocks[0],blocks[1],blocks[2]),shared=shared_mem)
		else:
			func(*self.cu_args,block=(threads[0],threads[1],threads[2]),grid=(blocks[0],blocks[1],blocks[2]))

	def start(self,args,arg_nam):
		try:
			import pycuda.driver as cuda
			import pycuda.autoinit
		except:
			return
		self.args = args
		self.nam_args = arg_nam
		self.argl = len(args)
		for i in range(len(args)):
			self.cu_args.append(cuda.mem_alloc(args[i].nbytes))
			cuda.memcpy_htod(self.cu_args[i],self.args[i])

	def flags(self):
		for i in self.nam_args:
			self.is_alloc.append(False)
			if self.nam_returns.count(i) == 1:
				self.id_ret.append(self.nam_args.index(i))

	def dfree(self):
		import pycuda.driver as cuda
		import pycuda.autoinit
		for arg in self.cu_args:
			arg.free()
			self.cu_args.pop(0)

	def get_cu_args(self):
		return self.cu_args[:]

	def get_returns(self,returns):
		self.retl = len(returns)
		self.nam_returns = returns
		self.flags()
		self.dtoh()
#		self.dfree()
		return self.returns

	def dtoh(self):
		import pycuda.driver as cuda
		import pycuda.autoinit
		for i in range(len(self.id_ret)):
			self.returns.append(self.args[self.id_ret[i]])
			cuda.memcpy_dtoh(self.returns[i],self.cu_args[self.id_ret[i]])


# End of File
