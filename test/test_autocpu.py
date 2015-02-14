# The cpu test file

import cpu

def Urutu(arg):
    def wrap(fn):
        if arg == "cpu":
            def inner(*args, **kargs):
                print fn,args
                cpu_ = cpu.cpu_run(fn,args)
                return cpu_.run()
        return inner
    return wrap


@Urutu("cpu")
def run(a,b,c):
    __shared is x
    c[tx] = a[tx] + b[tx]
    print c[tx]
    if 1 < 2:
        print "LOL"
    return c

if __name__ == "__main__":
    a = [1,2,3,4]
    b = [4,3,2,1]
    c = [0,0,0,0]
    c = run([len(a),1,1],[1,1,1],a,b,c)
