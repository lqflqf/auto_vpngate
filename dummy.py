from multiprocessing import Pool
import time

def d(e):
    time.sleep(2)
    return e*2

def g():
    i = 0
    while i < 20:
        yield i
        i += 1

def h(e):
    print('good')
    print(e)

def i(e):
    print('bad')
    print(e)

l = [i for i in range(5)]



if __name__ == '__main__':
    now = time.time()
    with Pool() as p:
        pm = p.map_async(d,iterable=l, callback=h, error_callback=i)
        #print(time.time() - now)
        print('sleeping')
        time.sleep(10)
        print('end')



