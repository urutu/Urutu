# Developed by Aditya Atluri
# Date: 18 Jan 2014
# Mail: pyurutu@gmail.com
# This file contains the OpenCL implementation of the Python Code
# It converts Python Code to OpenCL code
# Modified: 15 Jun 2014

import inspect,shlex
import numpy as np
import execl
import threads, blocks, declare, grammar
import device

class cl_test:
	arguments = []
	returns = []
	var_nam = []
	var_val = []
	kernel = "/**/"
	device = "/**/"
	threads = [1, 1, 1]
	blocks = [1, 1, 1]
	threads_dec = [False, False, False]
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
	num_return = 0
	count_return = 0
	is_device_code = False
	device_py = [[]]
	device_tab = 0
	device_body_buff = ""
	device_func_name = []
	device_var_nam = [[]]
	device_type_vars = [[]]
	device_scope = False
	device_sentences = [[]]
	device_threads_dec = [False,False,False]
	device_blocks_dec = [False, False, False]

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
			phrase.pop(0)
			for word in phrase:
				if word != ',':
					self.__global.append(word)
#			print self.__global
		if phrase[0] == '__shared' and phrase[1] == 'is':
			phrase.pop(0)
			phrase.pop(0)
			for word in phrase:
				if word != ',':
					self.__shared.append(word)
#			print self.__shared
		if phrase[0] == '__register' and phrase[1] == 'is':
			phrase.pop(0)
			phrase.pop(0)
			for word in phrase:
				if word != ',':
					self.__register.append(word)
#			print self.__register
		if phrase[0] == '__constant' and phrase[1] == 'is':
			phrase.pop(0)
			phrase.pop(0)
			for word in phrase:
				if word != ',':
					self.__constant.append(word)
#			print self.__constant

	def typeargs(self):
		for arg in self.args:
			j = str(type(arg[0])).split("'")
			if 'numpy' in j[1]:
				j = j[1].split(".")
				self.type_args.append(j[1]+"*")
				self.type_vars.append(j[1]+"*")
			else:
				self.type_args.append(j[0])
				self.type_vars.append(j[0])

	def funcname_cl(self, control):
		self.func_name = self.keys[control + 1]
		self.kernel = self.kernel + "__kernel void CL_kernel("
		return control + 2

	def semi_colon(self, phrase):
		self.kernel = self.kernel + phrase + ";\n"

	def declare_workitems(self,keys,kernel):
#		The keys are strings
#		print "\n\nDEC_WORKITEMS", keys, self.device_threads_dec, self.device_blocks_dec
		if keys.find('tx') > -1:
			kernel, self.device_threads_dec[0] = threads.tx(self.device_threads_dec[0], kernel)
		if keys.find('ty') > -1:
			kernel, self.device_threads_dec[1] = threads.ty(self.device_threads_dec[1], kernel)
		if keys.find('tz') > -1:
			kernel, self.device_threads_dec[2] = threads.tz(self.device_threads_dec[2], kernel)
		if keys.find('bx') > -1:
			kernel, self.device_blocks_dec[0] = blocks.bx(self.device_blocks_dec[0], kernel)
		if keys.find('bx') > -1:
			kernel, self.device_blocks_dec[1] = blocks.by(self.device_blocks_dec[1], kernel)
		if keys.find('bz') > -1:
			kernel, self.device_blocks_dec[2] = blocks.bz(self.device_blocks_dec[2], kernel)
		return kernel


	def inspect_it(self,sentence,kernel):
#		print "Inside inspect_it()",sentence,kernel
		phrase = sentence.split('\t')
		if phrase.count('#') > 0:
			return
		tab = phrase.count('')
##		if tab > self.tabs and tab != len(phrase):
#			for j in range(tab - self.tabs):
#				kernel = kernel + "{\n"
		if tab < self.tabs and tab != len(phrase):
			for j in range(self.tabs - tab):
				kernel = kernel + "}\n"
		self.tabs = phrase.count('')
		sh = shlex.shlex(phrase[-1])
		i = sh.get_token()
		if i == '@' or i == 'def' or i == '' or i == '#' or i == '//' or i == '"""':
			return kernel
		stmt = []
		while i is not sh.eof:
			stmt.append(i)
			i = sh.get_token()
#		print stmt
		for j in self.device_func_name:
			if stmt.count(j) > 0:
				kernel += self.device_create_func(self.device_func_name.index(j),j, stmt)
				kernel = self.device_body_buff + "}\n" + kernel
				self.device_body_buff = ""
				return kernel
		if self.keys.count('tx') > 0 or self.keys.count("__shared"):
			kernel, self.threads_dec[0] = threads.tx(self.threads_dec[0], kernel)
		if self.keys.count('ty') > 0:
			kernel, self.threads_dec[1] = threads.ty(self.threads_dec[1], kernel)
		if self.keys.count('tz') > 0:
			kernel, self.threads_dec[2] = threads.tz(self.threads_dec[2], kernel)
		if self.keys.count('bx') > 0:
			kernel, self.blocks_dec[0] = blocks.bx(self.blocks_dec[0], kernel)
		if self.keys.count('bx') > 0:
			kernel, self.blocks_dec[1] = blocks.by(self.blocks_dec[1], kernel)
		if self.keys.count('bz') > 0:
			kernel, self.blocks_dec[2] = blocks.bz(self.blocks_dec[2], kernel)
		if stmt.count('Tx') == 1 or stmt.count('Ty') == 1 or stmt.count('Tz') == 1:
			threads.threads_decl(stmt, self.var_nam, self.var_val, self.threads)
			return kernel
		if stmt.count('Bx') == 1 or stmt.count('By') == 1 or stmt.count('Bz') == 1:
			blocks.blocks_decl(stmt, self.var_nam, self.var_val, self.blocks)
			return kernel
		if stmt[0] == '__global' or stmt[0] == '__shared' or stmt[0] == '__register' or stmt[0] == '__constant' :
			self.decarrays(stmt)
			return kernel
		if stmt.count('if') > 0:
			return kernel + grammar.keyword(stmt, kernel)
		if stmt.count('else') > 0:
			kernel = kernel + "else"
		else:
#			print "Entering Checkvars"
			return self.checkvars(stmt,phrase[-1],kernel)
#		print stmt, self.tabs

	def device_create_func(self,index,name,stmt):
#		print "Inside DCF",name, stmt, self.device_py
		device_keys = self.device_py[index]
		self.device_scope = True
#		print "Device Keys",device_keys
		if stmt[stmt.index("(")+1] == "[" and stmt[stmt.index("(")+3] == "]":
			print "Dynamic Parallelism"
		else:
			self.device_funcname(stmt[:],device_keys[device_keys.index('(')+1:device_keys.index(')')],True)
#			print self.device_body_buff
#			print "Inititiate threads"
#			print stmt
			index = self.device_func_name.index(name)
			for i in self.device_sentences[index]:
				self.device_body_buff = self.declare_workitems(i,self.device_body_buff)
#			print "Inside CREATING DEVICE BODY"
			for i in self.device_sentences[index]:
				self.device_body_buff = self.inspect_it(i,self.device_body_buff)
#			print self.device_body_buff
		self.device_scope = False
		self.kernel = self.device_body_buff + self.kernel
		self.device_threads_dec = [False, False, False]
		self.device_blocks_dec = [False, False, False]
		return self.stringize(stmt) + "; \n"

	def device_funcname(self,stmt,args,device):
#		print "Inside device_funcname: ", stmt
		while ',' in args:
			args.remove(',')
		if device == True:
			self.device_body_buff = ""
		else:
			self.device_body_buff = "__global__ "
		index = stmt.index("(")
		tmp = " " + str(stmt[index-1]) + "("
		if self.device_func_name.count(stmt[0]) == 1:
			self.device_body_buff += "void "
		elif stmt[1] == "[":
			self.device_body_buff += self.type_vars[self.var_nam.index(stmt[0])][:-1]
		else:
			self.device_body_buff += self.type_vars[self.var_nam.index(stmt[0])]
		self.device_body_buff += tmp
#		print stmt,index
		idx = 0
		stmt[index], stmt[-1] = ',',','
		l=stmt.remove(stmt[0])
#		print args
		for j in range(len(stmt[index:])):
			i = stmt[j+index]
			if i is not ",":
#				print i
				if self.var_nam.count(i) == 1:
					if stmt[stmt.index(i)+1] == '[':
						type_var = self.type_vars[self.var_nam.index(i)][:-1]
						self.device_body_buff += type_var + " " + args[idx] + ", "
						self.device_var_nam[-1].append(args[idx])
						self.device_type_vars[-1].append(type_var)
					else:
						type_var = self.type_vars[self.var_nam.index(i)]
						if self.__shared.count(i) == 1:
							self.device_body_buff += "__local "
						elif self.__register.count(i) == 1:
							self.device_body_buff += "__private "
						elif self.__constant.count(i) == 1:
							self.device_body_buff += "__constant "
						else:
							self.device_body_buff += "__global "
						self.device_body_buff += type_var + " " + args[idx] + ", "
						self.device_var_nam[-1].append(args[idx])
						self.device_type_vars[-1].append(type_var)
				else:
					if stmt[j+1+index] is '.':
						self.device_body_buff += "float " + args[idx] + ", "
						j+=2
						self.device_var_nam[-1].append(args[idx])
						self.device_type_vars[-1].append("float")
					elif type(stmt[j]) is int or stmt[j] is '-':
						self.device_body_buff += "int " + args[idx] + ", "
						self.device_var_nam[-1].append(args[idx])
						self.device_type_vars[-1].append("int")
			else:
				idx += 1
		dec_threads = True
		self.device_body_buff = self.device_body_buff[:-2]
		self.device_body_buff +="){\n"
#		print "DBB",self.device_body_buff

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
	def decvars(self,stmt,phrase,kernel):
#		print "Inside Dec vars",kernel,phrase,stmt
		if kernel[-2] == '}':
			kernel = kernel[:-2]
#			kernel += "\n"
		if stmt.count('return') == 1:
			kernel += phrase+";\n"
#			print "Adding return",kernel
			return kernel
		elif stmt.count('=') == 0:
			return kernel
		else:
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
#					print "ret_checktype",ret_checktype
					kernel += ret_checktype[0] + ret_checktype[1] + ret_checktype[2] + " = " + ret_checktype[3] + ";\n"
#			print "Exiting decvars",kernel
			return kernel

#	CHECKVARS here!!
	def checkvars(self,stmt,phrase,kernel):
#		print "Inside Check Vars",phrase, stmt, kernel
		if self.__shared.count(stmt[0]) == 1 and self.var_nam.count(stmt[0]) == 0:
			kernel, self.var_nam, self.type_vars = declare.decshared(stmt, self.type_vars, self.var_nam, self.args, kernel)
			return kernel
		elif self.__global.count(stmt[0]) == 1 and self.var_nam.count(stmt[0]) == 0:
			kernel, self.var_nam, self.type_vars = declare.decglobal(stmt, self.type_vars, self.var_nam, self.args, kernel)
			return kernel
		elif self.__register.count(stmt[0]) == 1 and self.var_nam.count(stmt[0]) == 0:
			kernel, self.var_nam, self.type_vars = declare.decregister(stmt, self.type_vars, self.var_nam, self.args, kernel)
			return kernel
		elif self.__constant.count(stmt[0]) == 1 and self.var_nam.count(stmt[0]) == 0:
			kernel, self.var_nam, self.type_vars = declare.decconstant(stmt, self.type_vars, self.var_nam, self.args, kernel)
			return kernel
		else:
			kernel = self.decvars(stmt,phrase,kernel)
		return kernel

# body (self) here!
	def body(self):
		for sentence in self.sentences:
			if sentence.split('\t')>1:
				phrase = sentence.split('\t')
				tabs = phrase.count('')
#				print "Inside Body",phrase, tabs
				sh = shlex.shlex(phrase[-1])
				i = sh.get_token()
#				print i
				if i == "def":
#					print "In DEF"
#					print self.device_py
					self.is_device_code = True
					self.device_tab = tabs
					self.device_py.append([i])
					if self.device_py[0] == []:
						self.device_py.pop(0)
					i = sh.get_token()
					self.device_func_name.append(i)
#					print "DEC",self.device_func_name, self.device_py
					while i is not sh.eof:
						self.device_py[-1].append(i)
						i = sh.get_token()
					self.device_sentences.append([])
				elif self.device_tab < tabs and self.is_device_code == True:
					for j in phrase[tabs:]:
						self.device_sentences[-1].append(j)
					if self.device_sentences[0] == []:
						self.device_sentences.pop(0)
#					print "Body!!", self.device_py, self.device_sentences
				else:
					self.kernel = self.inspect_it(sentence,self.kernel)
		return

	def defargs(self,comma,control,kernel):
		if self.arguments.count(self.keys[control]) < 2:
			self.arguments.append(self.keys[control])
			if comma == True:
				if "int64*" == self.type_args[len(self.arguments) - 1]:
					kernel = kernel + ", __global long* " + self.keys[control]
					self.type_vars[len(self.arguments) - 1] = "long*"
				elif "int32*" == self.type_args[len(self.arguments) - 1]:
					kernel = kernel + ", __global int* " + self.keys[control]
					self.type_vars[len(self.arguments) - 1] = "int*"
				elif "float32*" == self.type_args[len(self.arguments) - 1]:
					kernel = kernel + ", __global float* " + self.keys[control]
					self.type_vars[len(self.arguments) - 1] = "float*"
				elif "float64*" == self.type_args[len(self.arguments) - 1]:
					kernel = kernel + ", __global double* " + self.keys[control]
					self.type_vars[len(self.arguments) - 1] = "double*"
				elif "int" == self.type_args[len(self.arguments) - 1]:
					kernel = kernel + ", int " + self.keys[control]
					self.type_vars[len(self.arguments) - 1] = "int"
				elif "float" == self.type_args[len(self.arguments) - 1]:
					kernel = kernel + ", float " + self.keys[control]
					self.type_vars[len(self.arguments) - 1] = "float"
			elif comma == False:
				if "int64*" == self.type_args[len(self.arguments) - 1]:
					kernel = kernel + " __global long* " + self.keys[control]
					self.type_vars[len(self.arguments) - 1] = "long*"
				elif "int32*" == self.type_args[len(self.arguments) - 1]:
					kernel = kernel + " __global int* " + self.keys[control]
					self.type_vars[len(self.arguments) - 1] = "int*"
				elif "float32*" == self.type_args[len(self.arguments) - 1]:
					kernel = kernel + " __global float* " + self.keys[control]
					self.type_vars[len(self.arguments) - 1] = "float*"
				elif "float64*" == self.type_args[len(self.arguments) - 1]:
					kernel = kernel + " __global double* " + self.keys[control]
					self.type_vars[len(self.arguments) - 1] = "double*"
				elif "int" == self.type_args[len(self.arguments) - 1]:
					kernel = kernel + " int " + self.keys[control]
					self.type_vars[len(self.arguments) - 1] = "int"
				elif "float" == self.type_args[len(self.arguments) - 1]:
					kernel = kernel + " float " + self.keys[control]
					self.type_vars[len(self.arguments) - 1] = "float"
			self.var_nam.append(self.keys[control])
		return kernel

	def execute(self):
		sh = shlex.shlex(self.code)
		i = sh.get_token()
		self.keys = [i]
		while i is not sh.eof:
			i = sh.get_token()
			self.keys.append(i)
		self.num_return = self.keys.count('return')
		control = self.keys.index('def')
		control = self.funcname_cl(control)
		comma = False
		if self.keys[control] == '(':
			control = control + 1
			while self.keys[control] != ')':
				if self.keys[control] == ',':
					control = control + 1
				self.kernel = self.defargs(comma, control, self.kernel)
				comma = True
				control = control + 1
			ret = len(self.keys) - self.keys[::-1].index('return')
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
		self.sentences.remove(self.sentences[1])
		self.sentences.remove(self.sentences[-2])
#		print self.kernel, "Entering body()"
		self.body()
		self.kernel = "#pragma OPENCL EXTENSION all : enable\n"+self.kernel + "}"
#		self.print_cl()
#		print self.var_nam, self.type_vars, self.__shared, self.__global
#		print self.kernel
		tmp = execl.cl_exe()
		return tmp.exe_cl(self.kernel, self.func_name, self.threads, self.blocks, self.args, self.returns)

	def print_cl(self):
		print "In print_cl:"
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

