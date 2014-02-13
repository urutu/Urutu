# Developed by Aditya Atluri
# Date: 18 Jan 2014
# Mail: pyurutu@gmail.com
# This file contains the execution of OpenCL code using PyOpenCL
# Modified: 10 Feb 2014

import inspect,shlex
import numpy as np
import execu

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
	type_vars = []
	words = []
	sentences = []
	__global = []
	__shared = []
	__register = []
	__constant = []
	tabs = 0

	def __init__(self,fn,args):
		stri = inspect.getsource(fn)
		sh = shlex.shlex(stri)
		self.code = stri
		self.args = args
		self.typeargs()

	def decvars(self, phrase):
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
		if self.threads_dec == False:
			self.threads_decl(stmt)
			return
		if self.blocks_dec == False:
			self.blocks_decl(stmt)
			return
		if stmt[0] == '__global' or stmt[0] == '__shared' or stmt[0] == '__register' or stmt[0] == '__constant' :
			self.decvars(stmt)
			return
		if stmt.count('if') > 0:
#			print "Going into IF... AKA void!"
			return
		else:
			self.checkvars(stmt,phrase[-1])
			return
#		print stmt, self.tabs

#	__constant here!!
	def decconstant(self, stmt):
		return
		print "In statement", stmt
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
		self.kernel = self.kernel + "__constant__ " + str(deftype) + " " + str(stmt[0]) + "[" + str(arraysize) + "];\n" + str(stmt[0]) + "[tx] = " + str(stmt[index]) + "[tx + " + str(startindex) + "];\n"
		self.var_nam.append(stmt[index - 1])

#	__global here!!
	def decglobal(self,stmt):
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
		self.kernel = "__device__ " + str(deftype) + " " + str(stmt[0]) + "[" + str(arraysize) + "];\n" + self.kernel + str(stmt[0]) + "[tx] = " + str(stmt[index]) + "[tx + " + str(startindex) + "];\n"
		self.var_nam.append(stmt[index - 1])

#	__shared is here!!
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
		self.var_nam.append(stmt[index - 1])

#	__register here!!!
	def decregister(self,stmt):
#		print "In decregister", stmt
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
		self.kernel = self.kernel + "__local__ " + str(deftype) + " " + str(stmt[0]) + "[" + str(arraysize) + "];\n" + str(stmt[0]) + "[tx] = " + str(stmt[index]) + "[tx + " + str(startindex) + "];\n"
		self.var_nam.append(stmt[index - 1])

	def checkvars(self,stmt,phrase):
		if self.__shared.count(stmt[0]) == 1 and self.var_nam.count(stmt[0]) == 0:
			self.decshared(stmt)
		elif self.__global.count(stmt[0]) == 1 and self.var_nam.count(stmt[0]) == 0:
			self.decglobal(stmt)
		elif self.__register.count(stmt[0]) == 1 and self.var_nam.count(stmt[0]) == 0:
			self.decregister(stmt)
		elif self.__constant.count(stmt[0]) == 1 and self.var_nam.count(stmt[0]) == 0:
			self.decconstant(stmt)
		else:
			self.kernel = self.kernel + str(phrase) + ";\n"

	def body(self):
		for sentence in self.sentences:
			if sentence.split('\t')!=-1:
				self.inspect_it(sentence)

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
#		self.print_cu()
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
		print self.threads_dec
		print self.blocks_dec
		print self.func_name
		print self.code
		print self.words
		print self.sentences

