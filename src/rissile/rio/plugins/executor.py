# To change this license header, choose License Headers in Project Properties.
# To change this template file, choose Tools | Templates
# and open the template in the editor.

__author__="K. Kulikov"
__date__ ="$Nov 24, 2014 10:54:30 PM$"


def g(arg):
    while True:
        print('df')
    return None

def f(args):
    from multiprocessing import Pool, cpu_count
    pool = Pool(processes=cpu_count())
    pool.map(g, (234, 234, 234, 234))
    pool.close()
    pool.join()
        
        
        
        
        
