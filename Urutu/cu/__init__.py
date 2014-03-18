# Developed by Aditya Atluri
# Date: 18 Jan 2014
# Mail: pyurutu@gmail.com
# This file contains the execution of OpenCL code using PyOpenCL
# This file converts Python code to CUDA code
# Modified: 20 Feb 2014

import inspect,shlex
import numpy as np
import execu
import threads, blocks, declare, grammar

class cu_test:
	arguments = []
	returns = []
	var_nam = []
	var_val = []
	kernel = "/**/"
	threads = [1, 1, 1]
	threads_dec = [False, False, False]
	blocks = [1, 1, 1]
	blocks_dec = [False, False, False]
	func_name = []
	code = ""
	args = []
	type_args = []
	type_vars = []
	words = []
	sentences = []
	__global = []
	__shared = []
	__register = []
	__constant = []
	tabs = 0

	def __init__(self, fn, args):
		stri = inspect.getsource(fn)
		sh = shlex.shlex(stri)
		self.code = stri
		self.args = args
		if type(self.args[0]) is list and type(self.args[1]) is not list:
			self.threads = self.args[0]
			self.args = self.args[1:]
		if type(self.args[0]) is list and type(self.args[1]) is list:
			self.threads = self.args[0]
			self.blocks = self.args[1]
			self.args = self.args[2:]
		self.typeargs()

	def decarrays(self, phrase):
#		print phrase
		if phrase[0] == '__global' and phrase[1] == 'is':
			phrase.pop(0)
			for word in phrase:
				if word != ',':
					self.__global.append(word)
#			print self.__global
		if phrase[0] == '__shared' and phrase[1] == 'is':
			phrase.pop(0)
			for word in phrase:
				if word != ',':
					self.__shared.append(word)
#			print self.__shared
		if phrase[0] == '__register' and phrase[1] == 'is':
			phrase.pop(0)
			for word in phrase:
				if word != ',':
					self.__register.append(word)
#			print self.__register
		if phrase[0] == '__constant' and phrase[1] == 'is':
			phrase.pop(0)
			for word in phrase:
				if word != ',':
					self.__constant.append(word)
#			print self.__constant

	def typeargs(self):
		for arg in self.args:
			j = str(type(arg[0])).split(".")
			j = j[1].split("'")
			self.type_args.append(j[0])
			self.type_vars.append(j[0])

	def funcname_cu(self,control):
		self.func_name = self.keys[control + 1]
		self.kernel = self.kernel+"__global__ void " + self.keys[control + 1] + "("
		return control + 2

	def semi_colon(self,phrase):
		self.kernel = self.kernel + phrase + ";\n"

	def inspect_it(self,sentence):
		phrase = sentence.split('\t')
		if phrase.count('#') > 0:
			return
		tab = phrase.count('')
		if tab > self.tabs:
			for j in range(tab - self.tabs):
				self.kernel = self.kernel + "{\n"
		if tab < self.tabs:
			for j in range(self.tabs - tab):
				self.kernel = self.kernel + "}\n"
		self.tabs = phrase.count('')
		sh = shlex.shlex(phrase[-1])
		i = sh.get_token()
		if i == 'def' or i == '@' or i == 'return' or i == '' or i == '#' or i == '//' or i == '"""':
			return
		stmt = []
		while i is not sh.eof:
			stmt.append(i)
			i = sh.get_token()
		if self.keys.count('tx') > 0:
			self.kernel, self.threads_dec[0] = threads.tx(self.threads_dec[0],self.kernel)
		if self.keys.count('ty') > 0:
			self.kernel, self.threads_dec[1] = threads.ty(self.threads_dec[1],self.kernel)
		if self.keys.count('tz') > 0:
			self.kernel, self.threads_dec[2] = threads.tz(self.threads_dec[2],self.kernel)
		if self.keys.count('bx') > 0:
			self.kernel, self.blocks_dec[0] = blocks.bx(self.blocks_dec[0], self.kernel)
		if self.keys.count('bx') > 0:
			self.kernel, self.blocks_dec[1] = blocks.by(self.blocks_dec[1], self.kernel)
		if self.keys.count('bz') > 0:
			self.kernel, self.blocks_dec[2] = blocks.bz(self.blocks_dec[2], self.kernel)
		if stmt.count('Tx') == 1 or stmt.count('Ty') == 1 or stmt.count('Tz') == 1:
			threads.threads_decl(stmt, self.var_nam, self.var_val, self.threads)
			return
		if stmt.count('Bx') == 1 or stmt.count('By') == 1 or stmt.count('Bz') == 1:
			blocks.blocks_decl(stmt, self.var_nam, self.var_val, self.blocks)
			return
		if stmt[0] == '__global' or stmt[0] == '__shared' or stmt[0] == '__register' or stmt[0] == '__constant' :
			self.decarrays(stmt)
			return
		if stmt.count('if') > 0:
			self.kernel = self.kernel + grammar._if.__init__(stmt, self.kernel)
			return
		if stmt.count('else') > 0:
			self.kernel = self.kernel + "else"
		else:
			self.checkvars(stmt,phrase[-1])
			return
#		print stmt, self.tabs



# Need to complete here!!
# Check whether the variables are declared or not.
	def checkchars(self, var):
		return False

# convert the list into string
	def stringize(self, stmt):
		phrase = ''
		for i in stmt:
			phrase = phrase + str(i)
		return phrase

# Checking the type of variable to be created
	def checktype(self,var,val):
#		print var, val
		if val.count('.') == 1:
			return 'float ', self.stringize(var[:]) , '',  self.stringize(val[:])
		try:
			int(self.stringize(val))
			return 'int ', self.stringize(var[:]), '', self.stringize(val[:])
		except:
			if self.stringize(val).find('"') != -1:
				return 'char ', self.stringize(var[:]), '[]',  self.stringize(val[:])
			elif self.stringize(val).find("'") != -1:
				val = str(val[0]).split("'")
				quote = ['"']
				quote.append(val[1])
				quote.append('"')
				return 'char ' , self.stringize(var[:]), '[]', self.stringize(quote)
			else:
				return '','',self.stringize(var[:]), self.stringize(val[:])

# a = 10 type variables are declared here!
	def decvars(self,stmt,phrase):
		ideq = stmt.index('=')
		commavarid = [-1]
		commavalid = [ideq]
		tmp = stmt
		for k in tmp:
			if k == ',' and tmp.index(k) < ideq:
				commavarid.append(tmp.index(k))
				tmp[tmp.index(k)] = ''
			if k == ',' and tmp.index(k) > ideq:
				commavalid.append(tmp.index(k))
				tmp[tmp.index(k)] = ''
		commacount = len(commavarid)
		commavalid.append(len(tmp))
		commavarid.append(ideq)
		for i in range(commacount):
			if self.var_nam.count(i) == 0 and stmt.index('=') > i:
				ret_checktype = self.checktype(stmt[commavarid[i]+1:commavarid[i+1]],stmt[commavalid[i]+1:commavalid[i+1]])
#				print ret_checktype
				self.kernel = self.kernel + ret_checktype[0] + ret_checktype[1] + ret_checktype[2] + " = " + ret_checktype[3] + ";\n"
		return

#	CHECKVARS here!!
	def checkvars(self,stmt,phrase):
		if self.__shared.count(stmt[0]) == 1 and self.var_nam.count(stmt[0]) == 0:
			self.kernel, self.var_nam = declare.decshared(stmt, self.type_vars, self.var_nam, self.args, self.kernel)
		elif self.__global.count(stmt[0]) == 1 and self.var_nam.count(stmt[0]) == 0:
			self.kernel, self.var_nam = declare.decglobal(stmt, self.type_vars, self.var_nam, self.args, self.kernel)
		elif self.__register.count(stmt[0]) == 1 and self.var_nam.count(stmt[0]) == 0:
			self.kernel, self.var_nam = declare.decregister(stmt, self.type_vars, self.var_nam, self.args, self.kernel)
		elif self.__constant.count(stmt[0]) == 1 and self.var_nam.count(stmt[0]) == 0:
			self.kernel, self.var_nam = declare.decconstant(stmt, self.type_vars, self.var_nam, self.args, self.kernel)
		else:
			self.decvars(stmt,phrase)
		return

# body (self) here!
	def body(self):
		for sentence in self.sentences:
			if sentence.split('\t')!=-1:
				self.inspect_it(sentence)
		return


	def defargs(self,comma,control):
		if self.arguments.count(self.keys[control]) < 2:
			self.arguments.append(self.keys[control])
			if comma == True:
				if "int64" == self.type_args[len(self.arguments) - 1]:
					self.kernel = self.kernel + ", long* " + self.keys[control]
					self.type_vars[len(self.arguments) - 1] = "long"
				elif "int32" == self.type_args[len(self.arguments) - 1]:
					self.kernel = self.kernel + ", int* " + self.keys[control]
					self.type_vars[len(self.arguments) - 1] = "int"
				elif "float32" == self.type_args[len(self.arguments) - 1]:
					self.kernel = self.kernel + ", float* " + self.keys[control]
					self.type_vars[len(self.arguments) - 1] = "float"
				elif "float64" == self.type_args[len(self.arguments) - 1]:
					self.kernel = self.kernel + ", double* " + self.keys[control]
					self.type_vars[len(self.arguments) - 1] = "double"
			elif comma == False:
				if "int64" == self.type_args[len(self.arguments) - 1]:
					self.kernel = self.kernel + " long* " + self.keys[control]
					self.type_vars[len(self.arguments) - 1] = "long"
				elif "int32" == self.type_args[len(self.arguments) - 1]:
					self.kernel = self.kernel + " int* " + self.keys[control]
					self.type_vars[len(self.arguments) - 1] = "int"
				elif "float32" == self.type_args[len(self.arguments) - 1]:
					self.kernel = self.kernel + " float* " + self.keys[control]
					self.type_vars[len(self.arguments) - 1] = "float"
				elif "float64" == self.type_args[len(self.arguments) - 1]:
					self.kernel = self.kernel + " double* " + self.keys[control]
					self.type_vars[len(self.arguments) - 1] = "double"
			self.var_nam.append(self.keys[control])

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
			self.kernel = self.kernel + ")\n"
			control = control + 1
		if self.keys[control] == ':':
			control = control + 1
		self.sentences = self.code.split("\n")
		self.body()
		self.kernel = self.kernel + "}"
		self.print_cu()
		tmp = execu.cu_exe()
		return tmp.exe_cu(self.kernel, self.func_name, self.threads, self.blocks, self.args, self.returns)

	def print_cu(self):
		print "In print_cu:"
		print self.type_args
		print self.arguments
		print self.returns
		print self.var_nam
		print self.var_val
		print self.kernel
		print self.threads
		print self.blocks
		print self.func_name
		print self.code
		print self.words
		print self.sentences

