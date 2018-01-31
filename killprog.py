#!/usr/bin/env python3
import re
import subprocess

hitlist = ["papserver", "pdpserver", "fps", "ffs", "coredns"]

# assert one pid per program name
pidprog = '(\d*)\/%s'
def get_pid(progs, netinfo):
    pids = []
    for prog in progs:
        m = re.search(pidprog % (prog), netinfo)
        pid = m.group(1)
        if pid is not None:
            pids.append(pid)
    return pids

def main():
    nstatcmd = 'netstat -plnt'
    killcmd = 'kill %s'
    stat = subprocess.check_output(nstatcmd.split())
    pids = get_pid(hitlist, stat)
    for pid in pids:
        killpid = killcmd % (pid)
        subprocess.Popen(killpid.split(), stdout=subprocess.PIPE)

if __name__ == '__main__':
    main()
