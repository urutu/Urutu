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
	returns = []
	nam_returns = []
	argl = 0
	retl = 0
	arg_nam = []
	id_ret_args = []
	id_ret_ret = []
	def exe_cl(self,stringg,func_name,threads,blocks,args,returns,arg_nam):
#		print returns
		self.args = args
		self.nam_returns = returns
		self.argl = len(args)
		self.retl = len(returns)
		self.arg_nam = arg_nam
		self.allocargs()
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
		for i in range(len(self.id_ret_ret)):
			cl.enqueue_copy(self.queue,self.returns[self.id_ret_ret[i]],self.cl_args[self.id_ret_args[i]])
		return


# End of File
