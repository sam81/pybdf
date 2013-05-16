#! /usr/bin/env python
# -*- coding: utf-8 -*-

from distutils.core import setup
setup(name="pybdf",    
    version="0.1.6",
      py_modules=["pybdf"],
      author="Samuele Carcagno",
      author_email="sam.carcagno@google.com;",
      description="pybdf is a python library for reading BIOSEMI bdf files.",
      long_description=\
      """
      pybdf provides python functions to read BIOSEMI 24-bit BDF files (used for storing electroencephalographic recordings)
      While being slower than alternative C-based libraries like BioSig http://biosig.sourceforge.net/, it is very easy to install and use.
      The software is currently in **ALPHA** status. 
      """,
      license="GPL v3",
      url="none",
      requires=['numpy (>=1.6.1)'],
      classifiers=[
          'Development Status :: 3 - Alpha',
          'Environment :: Console',
          'Intended Audience :: Developers',
          'License :: OSI Approved :: GNU General Public License v3 (GPLv3)',
          'Operating System :: MacOS :: MacOS X',
          'Operating System :: Microsoft :: Windows',
          'Operating System :: POSIX',
          'Programming Language :: Python :: 3.2',
          'Topic :: Scientific/Engineering :: Bio-Informatics'
          ]
      )
