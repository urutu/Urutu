<<<<<<< HEAD
=======
<<<<<<< HEAD
>>>>>>> ca74d31481b6ca65fa42ccf385776ad3b596044b
# Developed by Aditya Atluri
# Date: 18 Jan 2014
# Mail: pyurutu@gmail.com
# This file contains the execution of OpenCL code using PyOpenCL
# Modified: 9 Feb 2014

<<<<<<< HEAD
=======
=======
>>>>>>> e753cdd11a2374780ab952193b267bde32bfca02
>>>>>>> ca74d31481b6ca65fa42ccf385776ad3b596044b
import inspect,shlex
import numpy as np
import execu

<<<<<<< HEAD
=======
<<<<<<< HEAD
>>>>>>> ca74d31481b6ca65fa42ccf385776ad3b596044b
class cu_test:
	arguments = []
	returns = []
	var_nam = []
	var_val = []
	kernel = "/**/"
	threads = []
	blocks = []
	threads_dec = False
	blocks_dec = False
	func_name = []
	code = ""
	args = []
	type_args = []
<<<<<<< HEAD
	type_vars = []
	words = []
	sentences = []
	__global = []
	__shared = []
	__private = []
	__constant = []
	tabs = 0
=======
	words = []
	sentences = []
>>>>>>> ca74d31481b6ca65fa42ccf385776ad3b596044b

	def __init__(self,fn,args):
		stri = inspect.getsource(fn)
		sh = shlex.shlex(stri)
		self.code = stri
<<<<<<< HEAD
		self.args = args
		self.typeargs()

	def decvars(self, phrase):
		phrase.pop(1)
		if phrase[0] == '__global':
			phrase.pop(0)
			for word in phrase:
				if word != ',':
					self.__global.append(word)
#			print self.__global
		if phrase[0] == '__shared':
			phrase.pop(0)
			for word in phrase:
				if word != ',':
					self.__shared.append(word)
#			print self.__shared
		if phrase[0] == '__private':
			phrase.pop(0)
			for word in phrase:
				if word != ',':
					self.__private.append(word)
#			print self.__private
		if phrase[0] == '__constant':
			phrase.pop(0)
			for word in phrase:
				if word != ',':
					self.__constant.append(word)
#			print self.__constant

=======
=======
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
>>>>>>> e753cdd11a2374780ab952193b267bde32bfca02
		self.args = args
		self.typeargs()

>>>>>>> ca74d31481b6ca65fa42ccf385776ad3b596044b
	def typeargs(self):
		for arg in self.args:
			j = str(type(arg[0])).split(".")
			j = j[1].split("'")
			self.type_args.append(j[0])
<<<<<<< HEAD
			self.type_vars.append(j[0])

=======

<<<<<<< HEAD
>>>>>>> ca74d31481b6ca65fa42ccf385776ad3b596044b
	def funcname_cu(self,control):
		self.func_name = self.keys[control + 1]
		self.kernel = self.kernel+"__global__ void " + self.keys[control + 1] + "("
		return control + 2

	def semi_colon(self,phrase):
		self.kernel = self.kernel + phrase + ";\n"

<<<<<<< HEAD
	def inspect_it(self,sentence):
		phrase = sentence.split('\t')
		tab = phrase.count('')
		if tab > self.tabs:
			for j in range(tab - self.tabs):
				self.kernel = self.kernel + "{\n"
		if tab < self.tabs:
			for j in range(self.tabs - tab):
				self.kernel = self.kernel + "}\n"
		self.tabs = phrase.count('')
		sh = shlex.shlex(phrase[-1])
=======
	def inspect_it(self,phrase):
		sh = shlex.shlex(phrase)
>>>>>>> ca74d31481b6ca65fa42ccf385776ad3b596044b
		i = sh.get_token()
		if i == 'def' or i == '@' or i == 'return' or i == '' or i == '#' or i == '//' or i == '"""':
			return
		stmt = []
		while i is not sh.eof:
			stmt.append(i)
			i = sh.get_token()
		if self.threads_dec == False:
			self.threads_decl(stmt)
			return
		if self.blocks_dec == False:
			self.blocks_decl(stmt)
			return
<<<<<<< HEAD
		if stmt[0] == '__global' or stmt[0] == '__shared' or stmt[0] == '__private' or stmt[0] == '__constant' :
			self.decvars(stmt)
			return
		if stmt.count('if') > 0:
#			print "Going into IF... AKA void!"
			return
		else:
			self.checkvars(stmt,phrase[-1])
			return
#		print stmt, self.tabs

	def decshared(self,stmt):
#		print "In statement", stmt
		index = stmt.index('=') + 1
		deftype = self.type_vars[self.var_nam.index(stmt[index])]
#		print deftype
		if stmt.count(':') == 1:
			endindex = int(stmt[stmt.index(':') + 1])
			startindex = int(stmt[stmt.index(':') - 1])
			arraysize = int(endindex) - int(startindex)
		else:
			arraysize = self.args[self.var_nam.index(stmt[index])].size
			endindex = arraysize - 1
			startindex = 0
		self.kernel = self.kernel + "__shared__ " + str(deftype) + " " + str(stmt[0]) + "[" + str(arraysize) + "];\n" + str(stmt[0]) + "[tx] = " + str(stmt[index]) + "[tx + " + str(startindex) + "];\n"		

	def checkvars(self,stmt,phrase):
		if self.__shared.count(stmt[0]) == 1 and self.var_nam.count(stmt[0]) == 0:
			self.decshared(stmt)
		else:
			self.kernel = self.kernel + str(phrase) + ";\n"

	def body(self):
		for sentence in self.sentences:
			if sentence.split('\t')!=-1:
				self.inspect_it(sentence)
=======
		self.semi_colon(phrase)
	
	def body(self):
		for sentence in self.sentences:
			if sentence.split('\t')!=-1:
				phrase = sentence.split('\t')
				self.inspect_it(phrase[-1])
>>>>>>> ca74d31481b6ca65fa42ccf385776ad3b596044b

	def threads_decl(self, stmt):
		equ = stmt.index('=')
		if self.var_nam.count('Tx') < 1 and stmt.count('Tx') == 1:
			pos = stmt.index('Tx')
			pos_val = stmt[pos + 1 + equ]
			self.var_nam.append(stmt[pos])
			self.var_val.append(int(pos_val))
			string = "int tx = threadIdx.x;\n"
			self.threads.append(int(pos_val))
			self.kernel = self.kernel + string
		if self.var_nam.count('Ty') < 1 and stmt.count('Ty') == 1:
			pos = stmt.index('Ty')
			pos_val = stmt[pos + 1 + equ]
			self.var_nam.append(stmt[pos])
			self.var_val.append(int(pos_val))
			string = "int ty = threadIdx.y;\n"
			self.threads.append(int(pos_val))
			self.kernel = self.kernel + string
		if self.var_nam.count('Tz') < 1 and stmt.count('Tz') == 1:
			pos = stmt.index('Tz')
			pos_val = stmt[pos + 1 + equ]
			self.var_nam.append(stmt[pos])
			self.var_val.append(int(pos_val))
			string = "int tz = threadIdx.z;\n"
			self.threads.append(int(pos_val))
			self.kernel = self.kernel + string
		if len(self.threads) == 3:
			self.threads_dec = True

	def blocks_decl(self, stmt):
		equ = stmt.index('=')
		if self.var_nam.count('Bx') < 1 and stmt.count('Bx') == 1:
			pos = stmt.index('Bx')
			pos_val = stmt[pos + 1 + equ]
			self.var_nam.append(stmt[pos])
			self.var_val.append(int(pos_val))
			string = "int bx = blockIdx.x;\n"
			self.blocks.append(int(pos_val))
			self.kernel = self.kernel + string
		if self.var_nam.count('By') < 1 and stmt.count('By') == 1:
			pos = stmt.index('By')
			pos_val = stmt[pos + 1 + equ]
			self.var_nam.append(stmt[pos])
			self.var_val.append(int(pos_val))
			string = "int by = blockIdx.y;\n"
			self.blocks.append(int(pos_val))
			self.kernel = self.kernel + string
		if self.var_nam.count('Bz') < 1 and stmt.count('Bz') == 1:
			pos = stmt.index('Bz')
			pos_val = stmt[pos + 1 + equ]
			self.var_nam.append(stmt[pos])
			self.var_val.append(int(pos_val))
			string = "int bz = blockIdx.z;\n"
			self.blocks.append(int(pos_val))
			self.kernel = self.kernel + string
		if len(self.blocks) == 3:
			self.blocks_dec = True

	def defargs(self,comma,control):
		if self.arguments.count(self.keys[control]) < 2:
			self.arguments.append(self.keys[control])
			if comma == True:
				if "int64" == self.type_args[len(self.arguments) - 1]:
					self.kernel = self.kernel + ", long* " + self.keys[control]
<<<<<<< HEAD
					self.type_vars[len(self.arguments) - 1] = "long"
=======
>>>>>>> ca74d31481b6ca65fa42ccf385776ad3b596044b
				elif "int32" == self.type_args[len(self.arguments) - 1]:
					self.kernel = self.kernel + ", int* " + self.keys[control]
				elif "float32" == self.type_args[len(self.arguments) - 1]:
					self.kernel = self.kernel + ", float* " + self.keys[control]
				elif "float64" == self.type_args[len(self.arguments)-1]:
					self.kernel = self.kernel + ", double* " + self.keys[control]
			elif comma == False:
				if "int64" == self.type_args[len(self.arguments) - 1]:
					self.kernel = self.kernel + " long* " + self.keys[control]
<<<<<<< HEAD
					self.type_vars[len(self.arguments) - 1] = "long"
=======
>>>>>>> ca74d31481b6ca65fa42ccf385776ad3b596044b
				elif "int32" == self.type_args[len(self.arguments) - 1]:
					self.kernel = self.kernel + " int* " + self.keys[control]
				elif "float32" == self.type_args[len(self.arguments) - 1]:
					self.kernel = self.kernel + " float* " + self.keys[control]
				elif "float64" == self.type_args[len(self.arguments) - 1]:
					self.kernel = self.kernel + " double* " + self.keys[control]
<<<<<<< HEAD
			self.var_nam.append(self.keys[control])
=======
>>>>>>> ca74d31481b6ca65fa42ccf385776ad3b596044b

	def execute(self):
		sh = shlex.shlex(self.code)
		i = sh.get_token()
		self.keys = [i]
		while i is not sh.eof:
			i = sh.get_token()
			self.keys.append(i)
		control = self.keys.index('def')
		control = self.funcname_cu(control)
		comma = False
		if self.keys[control] == '(':
			control = control+1
			while self.keys[control] != ')':
				if self.keys[control] == ',':
					control = control + 1
				self.defargs(comma, control)
				comma = True
				control = control + 1
			ret = self.keys.index('return') + 1
			while self.keys[ret] != '':
				if self.keys[ret] == ',':
					ret = ret + 1
				self.returns.append(self.keys[ret])
				ret = ret + 1
<<<<<<< HEAD
			self.kernel = self.kernel + ")\n"
=======
			self.kernel = self.kernel + "){\n"
>>>>>>> ca74d31481b6ca65fa42ccf385776ad3b596044b
			control = control + 1
		if self.keys[control] == ':':
			control = control + 1
		self.sentences = self.code.split("\n")
		self.body()
		self.kernel = self.kernel + "}"
#		self.print_cu()
		tmp = execu.cu_exe()
		return tmp.exe_cu(self.kernel, self.func_name, self.threads, self.blocks, self.args, self.returns)
<<<<<<< HEAD
=======
=======
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
>>>>>>> e753cdd11a2374780ab952193b267bde32bfca02
>>>>>>> ca74d31481b6ca65fa42ccf385776ad3b596044b

	def print_cu(self):
		print "In print_cu:"
		print self.type_args
		print self.arguments
		print self.returns
<<<<<<< HEAD
		print self.var_nam
		print self.var_val
=======
<<<<<<< HEAD
		print self.var_nam
		print self.var_val
=======
		print self.variables_nam
		print self.variables_val
>>>>>>> e753cdd11a2374780ab952193b267bde32bfca02
>>>>>>> ca74d31481b6ca65fa42ccf385776ad3b596044b
		print self.kernel
		print self.threads
		print self.blocks
		print self.threads_dec
		print self.blocks_dec
		print self.func_name
		print self.code
<<<<<<< HEAD
		print self.words
		print self.sentences

=======
<<<<<<< HEAD
		print self.words
		print self.sentences

=======

def urutu_cu(fn):
	def inner(*args,**kargs):
		cu=cu_test(fn,args)
		return cu.execute()
	return inner
>>>>>>> e753cdd11a2374780ab952193b267bde32bfca02
>>>>>>> ca74d31481b6ca65fa42ccf385776ad3b596044b
