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
	arg_nam = []
	id_ret_args = []
	id_ret_ret = []
	def exe_cu(self,stringg,func_name,threads,blocks,args,returns,dyn_p,arg_nam):
		try:
			import pycuda.driver as cuda
			import pycuda.autoinit
			from pycuda.compiler import SourceModule
		except:
			return
		self.args = args
		self.nam_returns = returns
		self.argl = len(args)
		self.retl = len(returns)
		self.arg_nam = arg_nam
		self.allocargs()
		if dyn_p is True:
			mod=SourceModule(stringg, options=['-rdc=true'],linkers=['-lcudadevrt'])
		else:
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
		self.dfree()
		return self.returns

	def allocargs(self):
		import pycuda.driver as cuda
		import pycuda.autoinit
		for i in self.arg_nam:
			ind = self.arg_nam.index(i)
			if self.nam_returns.count(i) == 1:
				self.id_ret_ret.append(self.nam_returns.index(i))
				self.id_ret_args.append(self.arg_nam.index(i))
				self.returns.append(self.args[self.id_ret_args[-1]])
				self.cu_args.append(cuda.mem_alloc(self.args[ind].nbytes))
			else:
				self.cu_args.append(cuda.mem_alloc(self.args[ind].nbytes))
				cuda.memcpy_htod(self.cu_args[ind],self.args[ind])

	def dfree(self):
		import pycuda.driver as cuda
		import pycuda.autoinit
		for arg in self.cu_args:
			arg.free()
			self.cu_args.pop(0)

	def dtoh(self):
		import pycuda.driver as cuda
		import pycuda.autoinit
		for i in range(len(self.id_ret_ret)):
			cuda.memcpy_dtoh(self.returns[self.id_ret_ret[i]],self.cu_args[self.id_ret_args[i]])


# End of File
