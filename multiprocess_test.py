import time
from multiprocessing import Pool
import requests


def f3(e):
    return requests.head(e).status_code

def benchmark(f, p):
    print(f.__name__)
    now = time.time()
    f(p)
    print(time.time() - now)

def f1(p):
    print(list(map(f3, p)))

def f2(p):
    with Pool() as pool:
        print(pool.map(f3, p))

l = ["http://www.dmm.co.jp" for i in range(50)]

benchmark(f1, l)
benchmark(f2, l)
