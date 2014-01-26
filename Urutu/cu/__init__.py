import inspect,shlex
import numpy as np
import execu

_a=np.random.randint(10,size=100)
_b=np.random.randint(10,size=100)

class cu_test:
	arguments=[]
	returns=[]
	variables_nam=[]
	variables_val=[]
	kernel="/**/"
	threads=[]
	blocks=[]
	threads_dec=False
	blocks_dec=False
	func_name=[]
	code=""
	args = []
	type_args = []
	def __init__(self,fn,args):
		stri=inspect.getsource(fn)
		sh=shlex.shlex(stri)
		self.code=stri
		self.args = args
		self.typeargs()

	def typeargs(self):
		for arg in self.args:
			j = str(type(arg[0])).split(".")
			j = j[1].split("'")
			self.type_args.append(j[0])

	def print_funcname_cu(self,def_i,a):
		self.func_name=a[def_i+1]
		self.kernel=self.kernel+"__global__ void "+a[def_i+1]+"("
		return def_i+2

	def body_dev(self,stri_i):
		self.kernel=self.kernel+stri_i+";\n"

	def inspectit(self,stri_1):
		sh=shlex.shlex(stri_1)
		i=sh.get_token()
		if i=='def' or i=='@' or i=='return' or i=='':
			return
		stmt=[]
		while i is not sh.eof:
			stmt.append(i)
			i=sh.get_token()
		if self.threads_dec==False:
			self.threads_decl(stmt)
			return
		if self.blocks_dec==False:
			self.blocks_decl(stmt)
			return
		self.body_dev(stri_1)
	
	def print_numtabs(self,stri_3):
		for i in stri_3:
			if i.split('\t')!=-1:
				j= i.split('\t')
				self.inspectit(j[-1])

	def threads_decl(self,stmt):
		equ=stmt.index('=')
		if self.variables_nam.count('Tx')<1&stmt.count('Tx')==1:
			pos=stmt.index('Tx')
			pos_val=stmt[pos+1+equ]
			self.variables_nam.append(stmt[pos])
			self.variables_val.append(int(pos_val))
			stri_i="int tx = threadIdx.x;\n"
			self.threads.append(int(pos_val))
			self.kernel=self.kernel+stri_i
		if self.variables_nam.count('Ty')<1&stmt.count('Ty')==1:
			pos=stmt.index('Ty')
			pos_val=stmt[pos+1+equ]
			self.variables_nam.append(stmt[pos])
			self.variables_val.append(int(pos_val))
			stri_i="int ty = threadIdx.y;\n"
			self.threads.append(int(pos_val))
			self.kernel=self.kernel+stri_i
		if self.variables_nam.count('Tz')<1&stmt.count('Tz')==1:
			pos=stmt.index('Tz')
			pos_val=stmt[pos+1+equ]
			self.variables_nam.append(stmt[pos])
			self.variables_val.append(int(pos_val))
			stri_i="int tz = threadIdx.z;\n"
			self.threads.append(int(pos_val))
			self.kernel=self.kernel+stri_i
		if len(self.threads)==3:
			self.threads_dec=True

	def blocks_decl(self,stmt):
		equ=stmt.index('=')
		if self.variables_nam.count('Bx')<1&stmt.count('Bx')==1:
			pos=stmt.index('Bx')
			pos_val=stmt[pos+1+equ]
			self.variables_nam.append(stmt[pos])
			self.variables_val.append(int(pos_val))
			stri_i="int bx = blockIdx.x;\n"
			self.blocks.append(int(pos_val))
			self.kernel=self.kernel+stri_i
		if self.variables_nam.count('By')<1&stmt.count('By')==1:
			pos=stmt.index('By')
			pos_val=stmt[pos+1+equ]
			self.variables_nam.append(stmt[pos])
			self.variables_val.append(int(pos_val))
			stri_i="int by = blockIdx.y;\n"
			self.blocks.append(int(pos_val))
			self.kernel=self.kernel+stri_i
		if self.variables_nam.count('Bz')<1&stmt.count('Bz')==1:
			pos=stmt.index('Bz')
			pos_val=stmt[pos+1+equ]
			self.variables_nam.append(stmt[pos])
			self.variables_val.append(int(pos_val))
			stri_i="int bz = blockIdx.z;\n"
			self.blocks.append(int(pos_val))
			self.kernel=self.kernel+stri_i
		if len(self.blocks)==3:
			self.blocks_dec=True

	def print_variables(self,comma,var_i,a):
		if self.arguments.count(a[var_i])<2:
			self.arguments.append(a[var_i])
			if comma==True:
				if "int64" == self.type_args[len(self.arguments)-1]:
					stri=", long* "+a[var_i]
					self.kernel=self.kernel+stri
				elif "int32" == self.type_args[len(self.arguments)-1]:
					stri=", int* "+a[var_i]
					self.kernel=self.kernel+stri
				elif "float32" == self.type_args[len(self.arguments)-1]:
					stri=", float* "+a[var_i]
					self.kernel=self.kernel+stri
				elif "float64" == self.type_args[len(self.arguments)-1]:
					stri=", double* "+a[var_i]
					self.kernel=self.kernel+stri
			elif comma==False:
				if "int64" == self.type_args[len(self.arguments)-1]:
					stri=" long* "+a[var_i]
					self.kernel=self.kernel+stri
				elif "int32" == self.type_args[len(self.arguments)-1]:
					stri=" int* "+a[var_i]
					self.kernel=self.kernel+stri
				elif "float32" == self.type_args[len(self.arguments)-1]:
					stri=" float* "+a[var_i]
					self.kernel=self.kernel+stri
				elif "float64" == self.type_args[len(self.arguments)-1]:
					stri=" double* "+a[var_i]
					self.kernel=self.kernel+stri

	def execute(self):
		sh=shlex.shlex(self.code)
		i=sh.get_token()
		a=[i]
		while i is not sh.eof:
			i=sh.get_token()
			a.append(i)
		control=a.index('def')
		control=self.print_funcname_cu(control,a)
		comma=False
		if a[control]=='(':
			control=control+1
			while a[control]!=')':
				if a[control]==',':
					control=control+1
				self.print_variables(comma,control,a)
				comma=True
				control=control+1
			ret=a.index('return')+1
			while a[ret]!='':
				if a[ret]==',':
					ret=ret+1
				self.returns.append(a[ret])
				ret=ret+1
			self.kernel=self.kernel+"){\n"
			control=control+1
		if a[control]==':':
			control=control+1
		stri_1=self.code.split("\n")
		cu_test.print_numtabs(self,stri_1)
		self.kernel = self.kernel + "}"
#		self.print_cu()
		tmp = execu.cu_exe()
		return tmp.exe_cu(self.kernel,self.func_name,self.threads,self.blocks,self.args,self.returns)

	def print_cu(self):
		print "In print_cu:"
		print self.type_args
		print self.arguments
		print self.returns
		print self.variables_nam
		print self.variables_val
		print self.kernel
		print self.threads
		print self.blocks
		print self.threads_dec
		print self.blocks_dec
		print self.func_name
		print self.code

def urutu_cu(fn):
	def inner(*args,**kargs):
		cu=cu_test(fn,args)
		return cu.execute()
	return inner
