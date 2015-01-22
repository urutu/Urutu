# This file contains code that can be used later which cannot fit in right now.

'''This is the function to run 'map'. This is paused so that PyCUDA can support dynamic parallelism.

		if stmt.count('map') > 0:
			self.kernel_final.append(kernel+"}")
			start = stmt.index('map') + 2
			declar = self.device_py[self.device_func_name.index(stmt[start])]
			print declar, stmt
			caller = stmt[start+1:-1]
			called = declar[declar.index('('):-2]
			print caller, called
			end = len(stmt) - 1
			map_name = "map_" + str(stmt[start])
			print map_name
			self.map_func.append(map_name)
#			self.global_func.append(map_name)
			kernel  = "__device__ void " + map_name + "( "
			args = []
	#		print self.device_py, self.device_sentences, self.device_func_name, self.device_var_nam, self.device_type_vars
			for i in declar[3:-2]:
				if i != ",":
					args.append(i)
					kernel += str(self.type_vars[self.var_nam.index(caller[called.index(i)])]) + " " + str(i) + ","
#					print self.type_args, self.var_nam, self.type_args[self.var_nam.index(i)]
			kernel += str(self.type_vars[self.var_nam.index(stmt[0])]) + " " + str(stmt[0])
			kernel += "){\n" + "int tid = threadIdx.x + blockIdx.x * blockDim.x;\n"
			shh = shlex.shlex(self.device_sentences[self.device_func_name.index(stmt[start])][0])
			self.ismap.append(True)
			print self.type_vars
			kernel += stmt[0] + "[tid] = "
			print self.device_sentences[self.device_func_name.index(stmt[start])]
			if shh.get_token() == 'return':
				j = shh.get_token()
				while j is not shh.eof:
					if j in args:
						kernel += j + "[tid] "
					else:
						kernel += j
					j = shh.get_token()
			kernel += ";\n"
#			print kernel
#			print stmt[0]
			print "Printing Kernel", kernel
			return kernel'''

