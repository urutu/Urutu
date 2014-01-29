#!/usr/bin/env python

from distutils.core import setup

setup(name = 'Urutu',
	version = '0.1',
	description = 'A GPU based parallel programming library for Python',
	author = 'Aditya Atluri',
	author_email = 'adityaaatluri@gmail.com',
	url = 'https://github.com/urutu/Urutu',
	packages = ['Urutu','Urutu.cl','Urutu.cu'],
	license = 'Apache',
	)
