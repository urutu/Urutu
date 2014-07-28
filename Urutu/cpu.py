# The cpu lexical analysis file

import inspect,shlex

class cpu_run:
    keys = []
    code = ""
    threads = [1,1,1]
    blocks = [1,1,1]
    args = []
    sentences = []
    name = ""
    exec_args = []
    kernel = ""
    num_tabs = 1
    tab_len = 4
    run_args = []
    threads_for = [False, False, False]
    blocks_for = [False, False, False]
    def __init__(self, fn, args):
        stri = inspect.getsource(fn)
        self.code = stri
        if type(args[0]) is list and type(args[1]) is not list:
            self.threads = args[0]
            self.args = args[1:]
        if type(args[0]) is list and type(args[1]) is list:
            self.threads = args[0]
            self.blocks = args[1]
            self.args = args[2:]
        if args[0] == True:
            self.return_kernel = True
            self.args = args[1:]

    def declare_args(self):
        self.run_args = "("
        for i in self.str_args[1:-1]:
            if i is not ",":
                print i
                self.exec_args.append(str(i))
                self.run_args += str(i)
            else:
                self.run_args += str(i)
        self.run_args += ")"
        print self.run_args

    def lex(self):
        sh = shlex.shlex(self.code)
        i = sh.get_token()
        self.keys = [i]
        while i is not sh.eof:
            i = sh.get_token()
            self.keys.append(i)
        self.name = self.keys[self.keys.index("def")+1]
        self.sentences = self.code.split("\n")
        self.str_args = self.keys[self.keys.index(self.name)+1:self.keys.index(":")]
        print self.str_args
        self.declare_args()

    def diffuse(self):
        print "In diffuse"
        for sentence in self.sentences[:-1]:
            sh = shlex.shlex(sentence)
            i = sh.get_token()
            keys = [i]
            while i is not sh.eof:
                i = sh.get_token()
                keys.append(i)
            tabs = ""
            for i in range(len(sentence)):
                if sentence[i] is ' ':
                    tabs += ' '
                else:
                    break
            self.decl_workitems(keys,tabs,sentence)
        print "Out diffuse", self.kernel

    def decl_cache(self, keys, sentence):
        print keys
        if keys.count('__shared') > 0:
            print "In __shared"
            return
        elif keys.count("__global") > 0:
            return
        elif keys.count("__local") > 0:
            return
        else:
            self.kernel += sentence + "\n"

    def decl_workitems(self, keys, tabs, sentence):
        if keys.count("tx") > 0:
            print "In tx", keys
            if self.threads_for[0] == False:
                self.kernel += tabs + "for tx in range(" + str(self.threads[0]) + "):\n    " + tabs + sentence + "\n"
            elif self.threads_for[0] == True:
                self.kernel += tabs + "    " + sentence + "\n"
            self.threads_for[0] = True
            print self.threads_for[0]
        elif keys.count("ty") > 0:
            self.kernel += tabs + "for ty in range(" + str(self.threads[1]) + "):\n        " + tabs + sentence + "\n"
        else:
            self.decl_cache(keys, sentence)

    def run(self):
        self.code = self.code[13:]
        self.lex()
        self.diffuse()
        str_arg = str(self.args[0])
        for i in range(len(self.exec_args)):
            exec self.exec_args[i] + '=' + str(self.args[i])
            exec "print " + self.exec_args[i]
            print str(self.run_args)
        print self.kernel
        exec self.kernel
        exec self.name+str(self.run_args)
