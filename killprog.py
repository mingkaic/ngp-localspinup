#!/usr/bin/env python3
import re
import subprocess

hitlist = ["papserver", "pdpserver", "fps", "ffs", "coredns"]

# assert one pid per program name
pidprog = '(\d*)\/%s'

def format_extract(keys, format, info):
    valuemap = {}
    for key in keys:
        m = re.search(format % (key), info)
        if m is not None:
            value = m.group(1)
            if value is not None:
                valuemap[key] = value
    return valuemap

def command_extract(cmd, keys, format):
    stat = subprocess.check_output(cmd.split())
    return format_extract(keys, format, stat)

def main():
    nstatcmd = 'netstat -plnt'
    killcmd = 'kill %s'
    pidmap = command_extract(nstatcmd, hitlist, pidprog)
    for prog in pidmap:
        pid = pidmap[prog]
        killpid = killcmd % (pid)
        subprocess.Popen(killpid.split())

if __name__ == '__main__':
    main()
