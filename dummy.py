from multiprocessing import Pool


i = [(1,2), (3,4)]
def d(e):
    return e[0] + e[1]

if __name__ == '__main__':
    with Pool() as p:
        pm = p.map(d, i)
        print(pm)
