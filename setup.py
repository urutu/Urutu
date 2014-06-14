#!/usr/bin/env python

from distutils.core import setup

setup(name = 'Urutu',
	version = '1.0',
	description = 'A Python based parallel programming library for GPUs',
	author = 'Aditya Atluri',
	author_email = 'adityaaatluri@gmail.com',
	url = 'https://github.com/urutu/Urutu',
	packages = ['Urutu','Urutu.cl','Urutu.cu'],
	license = 'Apache',
	
	)
