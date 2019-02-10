import time
from multiprocessing import Pool
import aiohttp
import requests
import asyncio



def benchmark(func):
    def wrapper(*args):
        now = time.time()
        result = func(*args)
        print(time.time() - now)
        return result
    return wrapper


def fetch_sync(url):
    return requests.get(url).status_code

async def fetch_async(url):
    async with aiohttp.ClientSession() as session:
        async  with session.get(url) as response:
            return response.status

@benchmark
def process_sync(l):
    with Pool() as p:
        result = p.map(fetch_sync, l)
        print(result)

@benchmark
def process_async(l):
    loop = asyncio.get_event_loop()
    tasks = []

    for u in l:
        tasks.append(fetch_async(u))

    result = loop.run_until_complete(asyncio.gather(*tasks))
    print(result)
    loop.close()


if __name__ == '__main__':
    l = ['https://blog.jetbrains.com' for i in range(100)]

    print('sync')
    process_sync(l)

    print('async')
    process_async(l)





