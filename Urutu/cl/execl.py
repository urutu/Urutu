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
	def exe_cl(self,stringg,func_name,threads,blocks,args,returns):
#		print returns
		self.args = args
		argl = len(args)
		retl = len(returns)
#		print argl,retl
		self.allocargs(args,argl,retl)
		self.allocreturns(args,argl,retl)
		prg = cl.Program(self.ctx,stringg).build()
		if argl == 1:
			prg.CL_kernel(self.queue,threads,blocks, self.cl_args[0])
		elif argl == 2:
			prg.CL_kernel(self.queue,threads,blocks, self.cl_args[0], self.cl_args[1])
		elif argl == 3:
			prg.CL_kernel(self.queue,threads,blocks, self.cl_args[0], self.cl_args[1], self.cl_args[2])
		elif argl == 4:
			prg.CL_kernel(self.queue,threads,blocks, self.cl_args[0], self.cl_args[1], self.cl_args[2], self.cl_args[3])
		elif argl == 5:
			prg.CL_kernel(self.queue,threads,blocks, self.cl_args[0], self.cl_args[1], self.cl_args[2], self.cl_args[3], self.cl_args[4])
		elif argl == 6:
			prg.CL_kernel(self.queue,threads,blocks, self.cl_args[0], self.cl_args[1], self.cl_args[2], self.cl_args[3], self.cl_args[4], self.cl_args[5])
		elif argl == 7:
			prg.CL_kernel(self.queue,threads,blocks, self.cl_args[0], self.cl_args[1], self.cl_args[2], self.cl_args[3], self.cl_args[4], self.cl_args[5], self.cl_args[6])
		elif argl == 8:
			prg.CL_kernel(self.queue,threads,blocks, self.cl_args[0], self.cl_args[1], self.cl_args[2], self.cl_args[3], self.cl_args[4], self.cl_args[5], self.cl_args[6], self.cl_args[7])
		elif argl == 9:
			prg.CL_kernel(self.queue,threads,blocks, self.cl_args[0], self.cl_args[1], self.cl_args[2], self.cl_args[3], self.cl_args[4], self.cl_args[5], self.cl_args[6], self.cl_args[7], self.cl_args[8])
		elif argl == 10:
			prg.CL_kernel(self.queue,threads,blocks, self.cl_args[0], self.cl_args[1], self.cl_args[2], self.cl_args[3], self.cl_args[4], self.cl_args[5], self.cl_args[6], self.cl_args[7], self.cl_args[8], self.cl_args[9])
		self.copydtoh(args,argl,retl)
		if retl == 1:
			return self.args[argl - 1]
		elif retl == 2:
			return self.args[argl - 2], self.args[argl - 1]
		elif retl == 3:
			return self.args[argl - 3], self.args[argl - 2], self.args[argl - 1]
		elif retl == 4:
			return self.args[argl - 4], self.args[argl - 3], self.args[argl - 2], self.args[argl - 1]
		elif retl == 5:
			return self.args[argl - 5], self.args[argl - 4], self.args[argl - 3], self.args[argl - 2], self.args[argl - 1]
		elif retl == 6:
			return self.args[argl - 6], self.args[argl - 5], self.args[argl - 4], self.args[argl - 3], self.args[argl - 2], self.args[argl - 1]

	def allocargs(self,args,argl,retl):
		for i in range(argl-retl):
			self.cl_args.append(cl.Buffer(self.ctx, self.mf.READ_ONLY | self.mf.COPY_HOST_PTR, hostbuf=args[i]))

	def allocreturns(self,args,argl,retl):
		for i in range(retl):
			self.cl_args.append(cl.Buffer(self.ctx, self.mf.WRITE_ONLY, args[argl-retl+i].nbytes))

	def copydtoh(self,args,argl,retl):
		for i in range(retl):
			cl.enqueue_copy(self.queue,args[argl-retl+i],self.cl_args[argl-retl+i])


# End of File
