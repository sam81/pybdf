#! /usr/bin/env python
# -*- coding: utf-8 -*-

import os, platform, time

#get current version number from setup.py
f = open('../setup.py', 'r')
ln = f.readlines()
f.close()
for i in range(len(ln)):
    if ln[i].strip().split('=')[0].strip() == "version":
           ver = ln[i].strip().split('=')[1].strip()
           ver = ver[1:len(ver)-2]
tarball_path = "../dist/pybdf-" + ver + ".tar.gz"
buildpath = "../../pkg_build/" + platform.linux_distribution()[0] + '_' + platform.linux_distribution()[1] + '_' + platform.uname()[4]

if os.path.exists(buildpath) == False:
    os.makedirs(buildpath)

#copy tarball to the build directory
cmd = "cp " + tarball_path + " " + buildpath
os.system(cmd)

#update debian changelog
f = open('debian/changelog', 'r')
ln = f.readlines()
f.close()

l0 = ['pybdf (' + ver + ') unstable; urgency=low',
      '\n\n',
      '  * New upstream release',
      '\n\n',
      ' -- Samuele Carcagno <sam.carcagno@gmail.com>  ' + time.strftime("%a, %d %b %Y %H:%M:%S +0100", time.gmtime()),
      '\n\n']
l0.extend(ln)
f = open('debian/changelog', 'w')
ln = f.writelines(l0)
f.close()

#move to the build directory
os.chdir(buildpath)

#unpack the tarball
cmd2 = "tar -xvf " + "pybdf-" + ver + ".tar.gz"
os.system(cmd2)

#copy debian files in the package build directory
cmd3 = "cp -R " + "../../pybdf/prep-release/debian/ ./pybdf-" + ver
os.system(cmd3)

#move into package build directory
os.chdir("pybdf-" + ver)
#build the package
os.system("dpkg-buildpackage -F")
