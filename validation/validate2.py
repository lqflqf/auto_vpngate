from multiprocessing import Pool
from time import time
from os import cpu_count
from pathlib import Path
from subprocess import run, TimeoutExpired
from shutil import copy2

cmd = '/usr/local/Cellar/openvpn/2.4.6/sbin/openvpn'
op1 = '--config'
timeout = 10
folder = '/Users/qifan/vpngate_config'
vfolder = 'validated'


def run_cmd(path):

    try:
        result = run([cmd, op1, path.__str__()], timeout=timeout, capture_output=True)
    except TimeoutExpired as te:
        return None
    if 'Cannot allocate TUN/TAP dev dynamically' in result.stdout.decode('utf-8').split('\n')[-3]:
        print(path.__str__())
        return path
    else:
        return None


fp = Path(folder)
olist = list(fp.rglob('*.ovpn'))
now = time()
with Pool(cpu_count()) as pool:
    result = pool.map(run_cmd, olist)

for r in result:
    if r is not None:
        d = fp / vfolder / r.name
        if not d.exists():
            copy2(r.__str__(), d.__str__())


print(time()-now)

