# Developed by Aditya Atluri
# Date: 18 Jan 2014
# Mail: pyurutu@gmail.com
# Modified: 27 Jun 2014

from cl import cl_test
from cu import cu_test

def Urutu(arg):
	def wrap(fn):
		def inner(*args,**kargs):
			def import_cuda():
				cuda = False
				try:
					import pycuda
					cuda = True
				except:
					cuda = False
				return cuda
			def import_opencl():
				opencl = False
				try:
					import pyopencl
					opencl = True
				except:
					opencl = False
				return opencl
			if arg == "CL":
				cl_ = cl.cl_test(fn,args)
				return cl_.execute()
			elif arg == "CU":
				cu_ = cu.cu_test(fn,args)
				return cu_.execute()
			elif arg == "gpu":
				if import_cuda() is True:
					print "CUDA Found!"
					cu_ = cu.cu_test(fn,args)
					return cu_.execute()
				elif import_opencl() is True:
					print "CUDA API not supported on this machine"
					print "Switching to OpenCL..."
					cl_ = cl.cl_test(fn,args)
					return cl_.execute()
				else:
					print "CUDA and OpenCL APIs are not found in this machine."
					return
		return inner
	return wrap
