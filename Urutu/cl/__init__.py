# Developed by Aditya Atluri
# Date: 18 Jan 2014
# Mail: pyurutu@gmail.com
# This file contains the OpenCL implementation of the Python Code
# It converts Python Code to OpenCL code
# Modified: 9 Feb 2014

import inspect,shlex
import numpy as np
import execl

class cl_test:
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
	words = []
	sentences = []

	def __init__(self, fn, args):
		stri = inspect.getsource(fn)
		sh = shlex.shlex(stri)
		self.code = stri
		self.args = args
		self.typeargs()

	def typeargs(self):
		for arg in self.args:
			j = str(type(arg[0])).split(".")
			j = j[1].split("'")
			self.type_args.append(j[0])

	def funcname_cl(self, control):
		self.func_name = self.keys[control + 1]
		self.kernel = self.kernel + "__kernel void CL_kernel("
		return control + 2

	def semi_colon(self, phrase):
		self.kernel = self.kernel + phrase + ";\n"

	def inspect_it(self, phrase):
		sh = shlex.shlex(phrase)
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
		self.semi_colon(phrase)
	
	def body(self):
		for sentence in self.sentences:
			if sentence.split('\t')!=-1:
				phrase = sentence.split('\t')
				self.inspect_it(phrase[-1])

	def threads_decl(self, stmt):
		equ = stmt.index('=')
		if self.var_nam.count('Tx') < 1 and stmt.count('Tx') == 1:
			pos = stmt.index('Tx')
			pos_val = stmt[pos + 1 + equ]
			self.var_nam.append(stmt[pos])
			self.var_val.append(int(pos_val))
			string = "int tx = get_global_id(0);\n"
			self.threads.append(int(pos_val))
			self.kernel = self.kernel + string
		if self.var_nam.count('Ty') < 1 and stmt.count('Ty') == 1:
			pos = stmt.index('Ty')
			pos_val = stmt[pos + 1 + equ]
			self.var_nam.append(stmt[pos])
			self.var_val.append(int(pos_val))
			string = "int ty = get_global_id(1);\n"
			self.threads.append(int(pos_val))
			self.kernel = self.kernel + string
		if self.var_nam.count('Tz') < 1 and stmt.count('Tz') == 1:
			pos = stmt.index('Tz')
			pos_val = stmt[pos + 1 + equ]
			self.var_nam.append(stmt[pos])
			self.var_val.append(int(pos_val))
			string = "int tz = get_global_id(2);\n"
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
			string = "int bx = get_local_id(0);\n"
			self.blocks.append(int(pos_val))
			self.kernel = self.kernel + string
		if self.var_nam.count('By') < 1 and stmt.count('By') == 1:
			pos = stmt.index('By')
			pos_val = stmt[pos + 1 + equ]
			self.var_nam.append(stmt[pos])
			self.var_val.append(int(pos_val))
			string = "int by = get_local_id(1);\n"
			self.blocks.append(int(pos_val))
			self.kernel = self.kernel + string
		if self.var_nam.count('Bz') < 1 and stmt.count('Bz') == 1:
			pos = stmt.index('Bz')
			pos_val = stmt[pos + 1 + equ]
			self.var_nam.append(stmt[pos])
			self.var_val.append(int(pos_val))
			string = "int bz = get_local_id(2);\n"
			self.blocks.append(int(pos_val))
			self.kernel = self.kernel + string
		if len(self.blocks) == 3:
			self.blocks_dec = True

	def defargs(self,comma,control):
		if self.arguments.count(self.keys[control]) < 2:
			self.arguments.append(self.keys[control])
			if comma == True:
				if "int64" == self.type_args[len(self.arguments) - 1]:
					self.kernel = self.kernel + ", __global long* " + self.keys[control]
				elif "int32" == self.type_args[len(self.arguments) - 1]:
					self.kernel = self.kernel + ", __global int* " + self.keys[control]
				elif "float32" == self.type_args[len(self.arguments) - 1]:
					self.kernel = self.kernel + ", __global float* " + self.keys[control]
				elif "float64" == self.type_args[len(self.arguments) - 1]:
					self.kernel = self.kernel + ", __global double* " + self.keys[control]
			elif comma == False:
				if "int64" == self.type_args[len(self.arguments) - 1]:
					self.kernel = self.kernel + " __global long* " + self.keys[control]
				elif "int32" == self.type_args[len(self.arguments) - 1]:
					self.kernel = self.kernel + " __global int* " + self.keys[control]
				elif "float32" == self.type_args[len(self.arguments) - 1]:
					self.kernel = self.kernel + " __global float* " + self.keys[control]
				elif "float64" == self.type_args[len(self.arguments) - 1]:
					self.kernel = self.kernel + " __global double* " + self.keys[control]

	def execute(self):
		sh = shlex.shlex(self.code)
		i = sh.get_token()
		self.keys = [i]
		while i is not sh.eof:
			i = sh.get_token()
			self.keys.append(i)
		control = self.keys.index('def')
		control = self.funcname_cl(control)
		comma = False
		if self.keys[control] == '(':
			control = control + 1
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
			self.kernel = self.kernel + "){\n"
			control = control + 1
		if self.keys[control] == ':':
			control = control + 1
		self.sentences = self.code.split("\n")
		self.body()
		self.kernel = self.kernel + "}"
#		self.print_cl()
		tmp = execl.cl_exe()
		return tmp.exe_cl(self.kernel, self.func_name, self.threads, self.blocks, self.args, self.returns)

	def print_cl(self):
		print "In print_cl:"
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

