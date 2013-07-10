#! /usr/bin/env python
# -*- coding: utf-8 -*-

import getopt, datetime, os, subprocess, sys
os.chdir('../')

def main(argv):
    try:
        opts, args = getopt.getopt(argv, "m:", ["message="])
    except getopt.GetoptError:
        sys.exit(2)
    for opt, arg in opts:
        if opt in ("-m", "--message"):
            message = arg
    major_v = 0
    minor_v = 2

    f = open('prep-release/minor_minor_number.txt', 'r')
    ln = f.readlines()
    f.close()
    minor_minor_v = int(ln[0].strip()) + 1
    f = open('prep-release/minor_minor_number.txt', 'w')
    f.write(str(minor_minor_v))
    f.close()
    builddate = datetime.datetime.now().strftime("%d-%b-%Y %H:%M")
    gittag = str(major_v) + '.' + str(minor_v) + '.' + str(minor_minor_v)
    print(gittag)
    f = open('setup.py', 'r')
    ln = f.readlines()
    f.close()
    for i in range(len(ln)):
        if ln[i].strip().split('=')[0].strip() == "version":
            ln[i] = '    version="' + gittag +'",\n'

    f = open('setup.py', 'w')
    f.writelines(ln)
    f.close()

    f = open('pybdf.py', 'r')
    ln = f.readlines()
    f.close()
    for i in range(len(ln)):
        if ln[i].strip().split('=')[0].strip() == "__version__":
            ln[i] = '__version__ = "' + gittag +'"\n'

    f = open('pybdf.py', 'w')
    f.writelines(ln)
    f.close()


    f = open('doc/conf.py', 'r')
    ln = f.readlines()
    f.close()
    for i in range(len(ln)):
        if ln[i].strip().split('=')[0].strip() == "version":
            ln[i] = 'version = "' + gittag +'",\n'
        if ln[i].strip().split('=')[0].strip() == "release":
            ln[i] = 'release = "' + gittag + '",\n'

    f = open('doc/conf.py', 'w')
    f.writelines(ln)
    f.close()

 
    subprocess.call('git commit -a -m"' + message+'"', shell=True)
    subprocess.call('git tag -a "' + gittag +'"' + ' -m "' + gittag +'"', shell=True)
    
if __name__ == "__main__":
    main(sys.argv[1:])
