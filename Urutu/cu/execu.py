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
	def exe_cu(self,stringg,func_name,threads,blocks,args,returns,dyn_p,arg_nam):
#		print stringg, func_name, threads,blocks,args,returns,dyn_p,arg_nam
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
		self.nam_args = arg_nam
		self.flags()
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

	def initialize(self,args,nam_args):
		self.args = args
		self.nam_args = nam_args
		for i in range(len(nam_args)):
			self.cu_args.append([1])
			self.is_alloc.append(False)

	def allocargs(self):
		import pycuda.driver as cuda
		import pycuda.autoinit
#		print self.is_alloc
		for i in range(len(self.nam_args)):
			if self.is_alloc[i] == False:
				self.cu_args.append(cuda.mem_alloc(self.args[i].nbytes))
				cuda.memcpy_htod(self.cu_args[i],self.args[i])

	def discrete_alloc(self,var):
		import pycuda.driver as cuda
		import pycuda.autoinit
		if self.nam_args.count(var) > 0:
			i = self.nam_args.index(var)
			self.cu_args.append(cuda.malloc(self.args[self.nam_args.index(var)]))
			cuda.memcpy_htod(self.cu_args[i],self.args[i])
			return self.cu_args[i]

	def flags(self):
		for i in self.nam_args:
			self.is_alloc.append(False)
			if self.nam_returns.count(i) == 1:
				self.id_ret.append(self.nam_args.index(i))
#		print self.nam_args, self.id_ret, self.is_alloc

	def dfree(self):
		import pycuda.driver as cuda
		import pycuda.autoinit
		for arg in self.cu_args:
			arg.free()
			self.cu_args.pop(0)

	def dtoh(self):
		import pycuda.driver as cuda
		import pycuda.autoinit
#		print self.id_ret, self.cu_args
		for i in range(len(self.id_ret)):
			self.returns.append(self.args[self.id_ret[i]])
#			print self.args[i], self.returns[-1]
			cuda.memcpy_dtoh(self.returns[i],self.cu_args[self.id_ret[i]])


# End of File
