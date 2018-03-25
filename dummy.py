from multiprocessing import Pool



def d(e):
    return e*2

def g():
    i = 0
    while i < 10:
        yield i
        i += 1

l = (i for i in range(10))



if __name__ == '__main__':
    with Pool() as p:
        pm = p.map(d, g())
        print(pm)
