# Developed by Aditya Atluri
# Date: 18 Jan 2014
# Mail: pyurutu@gmail.com
# Modified: 27 Jun 2014

from cl import cl_test
from cu import cu_test

def Urutu(arg):
	def wrap(fn):
		def inner(*args,**kargs):
			if arg == "CL":
				cl_ = cl.cl_test(fn,args)
				return cl_.execute()
			elif arg == "CU":
				cu_ = cu.cu_test(fn,args)
				return cu_.execute()
			elif arg == "gpu":
				try:
					import pycuda
					print "Running on CUDA"
					cu_ = cu.cu_test(fn,args)
					return cu_.execute()
				except:
					print "CUDA API not supported on this machine"
					print "Switching to OpenCL"
					try:
						import pyopencl
						print "Running on OpenCL"
						cl_ = cl.cl_test(fn,args)
						return cl_.execute()
					except:
						print "Unable to import PyOpenCL"
			else:
				print "CUDA and OpenCL APIs are not found in this machine."
				return
		return inner
	return wrap
