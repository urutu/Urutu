from cl import *
from cu import *

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
