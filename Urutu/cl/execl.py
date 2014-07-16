# Developed by Aditya Atluri
# Date: 18 Jan 2014
# Mail: pyurutu@gmail.com
# This file contains the execution of OpenCL code using PyOpenCL
# Modified: 18 Jan 2014

import pyopencl as cl
import numpy as np
import numpy.linalg as la

class cl_exe:
	ctx = cl.create_some_context()
	queue = cl.CommandQueue(ctx)
	mf = cl.mem_flags
	cl_args = []
	args = []
	argl = 0
	retl = 0
	returns = []
	nam_returns = []
	nam_args = []
	id_ret = []
	is_alloc = []

	def exe_cl(self,stringg,func_name,threads,blocks):
		prg = cl.Program(self.ctx,stringg).build()
		if self.argl == 1:
			prg.CL_kernel(self.queue,threads,blocks, self.cl_args[0])
		elif self.argl == 2:
			prg.CL_kernel(self.queue,threads,blocks, self.cl_args[0], self.cl_args[1])
		elif self.argl == 3:
			prg.CL_kernel(self.queue,threads,blocks, self.cl_args[0], self.cl_args[1], self.cl_args[2])
		elif self.argl == 4:
			prg.CL_kernel(self.queue,threads,blocks, self.cl_args[0], self.cl_args[1], self.cl_args[2], self.cl_args[3])
		elif self.argl == 5:
			prg.CL_kernel(self.queue,threads,blocks, self.cl_args[0], self.cl_args[1], self.cl_args[2], self.cl_args[3], self.cl_args[4])
		elif self.argl == 6:
			prg.CL_kernel(self.queue,threads,blocks, self.cl_args[0], self.cl_args[1], self.cl_args[2], self.cl_args[3], self.cl_args[4], self.cl_args[5])
		elif self.argl == 7:
			prg.CL_kernel(self.queue,threads,blocks, self.cl_args[0], self.cl_args[1], self.cl_args[2], self.cl_args[3], self.cl_args[4], self.cl_args[5], self.cl_args[6])
		elif self.argl == 8:
			prg.CL_kernel(self.queue,threads,blocks, self.cl_args[0], self.cl_args[1], self.cl_args[2], self.cl_args[3], self.cl_args[4], self.cl_args[5], self.cl_args[6], self.cl_args[7])
		elif self.argl == 9:
			prg.CL_kernel(self.queue,threads,blocks, self.cl_args[0], self.cl_args[1], self.cl_args[2], self.cl_args[3], self.cl_args[4], self.cl_args[5], self.cl_args[6], self.cl_args[7], self.cl_args[8])
		elif self.argl == 10:
			prg.CL_kernel(self.queue,threads,blocks, self.cl_args[0], self.cl_args[1], self.cl_args[2], self.cl_args[3], self.cl_args[4], self.cl_args[5], self.cl_args[6], self.cl_args[7], self.cl_args[8], self.cl_args[9])

	def start(self,args,arg_nam):
		self.args = args
		self.nam_args = arg_nam
		self.argl = len(args)
		for i in range(self.argl):
			self.cl_args.append(cl.Buffer(self.ctx,self.mf.READ_WRITE | self.mf.COPY_HOST_PTR, hostbuf = self.args[i]))

	def flags(self):
		for i in self.nam_args:
			self.is_alloc.append(False)
			if self.nam_returns.count(i) == 1:
				self.id_ret.append(self.nam_args.index(i))

	def get_returns(self,returns):
		self.retl = len(returns)
		self.nam_returns = returns
		self.flags()
		self.copydtoh()
		return self.returns

	def allocargs(self):
		for i in self.arg_nam:
			if self.nam_returns.count(i) == 1:
				self.id_ret_ret.append(self.nam_returns.index(i))
				self.id_ret_args.append(self.arg_nam.index(i))
				self.returns.append(self.args[self.id_ret_args[-1]])
				self.cl_args.append(cl.Buffer(self.ctx, self.mf.WRITE_ONLY, self.args[self.arg_nam.index(i)].nbytes))
			else:
				self.cl_args.append(cl.Buffer(self.ctx, self.mf.READ_ONLY | self.mf.COPY_HOST_PTR, hostbuf=self.args[self.arg_nam.index(i)]))
		return


	def copydtoh(self):
		for i in range(len(self.id_ret)):
			self.returns.append(self.args[self.id_ret[i]])
			cl.enqueue_copy(self.queue,self.returns[i],self.cl_args[self.id_ret[i]])


# End of File
