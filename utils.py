import pprint as ppr
from time import time

def time_function(func):
    def wrapper(*args, **kwargs):
        tstart = time()
        res = func(*args, **kwargs)
        tstop = time()
        print(f"Execution of function {func.__name__} took {tstop - tstart}s (= {(tstop - tstart)/60.0}min)")
        return res
    return wrapper

def _pprint(d, indent=4, depth=1):
    pp = ppr.PrettyPrinter(indent=indent, depth=depth)
    pp.pprint(d)
