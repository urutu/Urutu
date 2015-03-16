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
#		print string, func_name
		if is_shared == True:
			func(*self.cu_args,block=(threads[0],threads[1],threads[2]),grid=(blocks[0],blocks[1],blocks[2]),shared=16*1024)
		else:
			func(*self.cu_args,block=(threads[0],threads[1],threads[2]),grid=(blocks[0],blocks[1],blocks[2]))

	def malloc(self,args,arg_nam):
		try:
			import pycuda.driver as cuda
			import pycuda.autoinit
		except:
			return
		print self.args
		self.args = args
		self.nam_args = arg_nam
		self.argl = len(args)
		for i in range(len(args)):
			self.cu_args.append(cuda.mem_alloc(args[i].nbytes))
		
	def htod(self,arg_nam):
		try:
			import pycuda.driver as cuda
			import pycuda.autoinit
		except:
			return
		index = self.nam_args.index(arg_nam)
		cuda.memcpy_htod(self.cu_args[index],self.args[index])

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

	def get_returns(self,returns,moved):
		for i in returns:
			if i in moved:
				self.dtoh(i)
			ret_id = self.nam_args.index(i)
			self.returns.append(self.args[ret_id])				
		return self.returns

	def dtoh(self,nam):
		try:
			import pycuda.driver as cuda
			import pycuda.autoinit
		except:
			return
		var_id = self.nam_args.index(nam)
		cuda.memcpy_dtoh(self.args[var_id], self.cu_args[var_id]);
#		cuda.memcpy_dtoh(self.returns[i],self.cu_args[self.id_ret[i]])


# End of File
