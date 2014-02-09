<<<<<<< HEAD
=======
<<<<<<< HEAD
>>>>>>> ca74d31481b6ca65fa42ccf385776ad3b596044b
# Developed by Aditya Atluri
# Date: 18 Jan 2014
# Mail: pyurutu@gmail.com
# This file contains the execution of OpenCL code using PyOpenCL
# Modified: 9 Feb 2014

from cl import cl_test
from cu import cu_test
<<<<<<< HEAD
=======
=======
from cl import *
from cu import *
>>>>>>> e753cdd11a2374780ab952193b267bde32bfca02
>>>>>>> ca74d31481b6ca65fa42ccf385776ad3b596044b

def Urutu(arg):
	def wrap(fn):
		def inner(*args,**kargs):
			if arg == "CL":
				cl_ = cl.cl_test(fn,args)
				return cl_.execute()
			elif arg == "CU":
				cu_ = cu.cu_test(fn,args)
				return cu_.execute()
			else:
				print "Not working!!"
				return
		return inner
	return wrap
