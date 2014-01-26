# Developed by Aditya Atluri
# Date: 18 Jan 2014
# Mail: pyurutu@gmail.com
# This file contains the execution of OpenCL code using PyOpenCL

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
	def exe_cl(self,stringg,func_name,threads,blocks,args,returns):
#		print returns
		self.args = args
		self.argl = len(args)
		self.retl = len(returns)
#		print argl,retl
		self.allocargs()
		self.allocreturns()
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
		if self.retl == 0:
			return 
		elif self.retl == 1:
			return self.args[self.argl - 1]
		elif self.retl == 2:
			return self.args[self.argl - 2], self.args[self.argl - 1]
		elif self.retl == 3:
			return self.args[self.argl - 3], self.args[self.argl - 2], self.args[self.argl - 1]
		elif self.retl == 4:
			return self.args[self.argl - 4], self.args[self.argl - 3], self.args[self.argl - 2], self.args[self.argl - 1]
		elif self.retl == 5:
			return self.args[self.argl - 5], self.args[self.argl - 4], self.args[self.argl - 3], self.args[self.argl - 2], self.args[self.argl - 1]
		elif self.retl == 6:
			return self.args[self.argl - 6], self.args[self.argl - 5], self.args[self.argl - 4], self.args[self.argl - 3], self.args[self.argl - 2], self.args[self.argl - 1]

	def allocargs(self):
		for i in range(self.argl-self.retl):
			self.cl_args.append(cl.Buffer(self.ctx, self.mf.READ_ONLY | self.mf.COPY_HOST_PTR, hostbuf=self.args[i]))

	def allocreturns(self):
		for i in range(self.retl):
			self.cl_args.append(cl.Buffer(self.ctx, self.mf.WRITE_ONLY, self.args[self.argl-self.retl+i].nbytes))

	def copydtoh(self):
		for i in range(self.retl):
			cl.enqueue_copy(self.queue,self.args[self.argl-self.retl+i],self.cl_args[self.argl-self.retl+i])


# End of File
