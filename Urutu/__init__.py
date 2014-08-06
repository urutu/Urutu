# Developed by Aditya Atluri
# Date: 18 Jan 2014
# Mail: pyurutu@gmail.com
# Modified: 27 Jun 2014

from cl import cl_test
from cu import cu_test

def Urutu(arg):
	def wrap(fn):
		def inner(*args,**kargs):
			def import_opencl():
				pyopencl = False
				try:
					import pyopencl
					pyopencl = True
				except:
					pyopencl = False
				return pyopencl
			def import_cuda():
				pycuda = False
				try:
					import pycuda
					pycuda = True
				except:
					pycuda = False
				return pycuda
			if arg == "CL":
				cl_ = cl.cl_test(fn,args)
				return cl_.execute()
			elif arg == "CU":
				cu_ = cu.cu_test(fn,args)
				return cu_.execute()
			elif arg == "gpu":
				if import_cuda() is True:
					cu__ = cu.cu_test(fn,args)
					return cu__.execute()
				else:
					print "CUDA is not found on this machine"
					print "Switching to OpenCL..."
					if import_opencl():
						cl__ = cl.cl_test(fn,args)
						print "PyOpenCL"
						return cl__.execute()
					else:
						print "CUDA and OpenCL are not found on this machine"
			else:
				print "CUDA and OpenCL APIs are not found in this machine."
				return
		return inner
	return wrap
