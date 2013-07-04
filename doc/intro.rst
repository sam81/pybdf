 
************
Introduction
************
:Author: Samuele Carcagno

pybdf is a python library to read BIOSEMI 24-bit BDF files.


*************************
Download and Installation
*************************

Download
========

The latest release of pybdf can be downloaded from the python package index:
 
http://pypi.python.org/pypi/pybdf/

For developers: the source code of pybdf is hosted on
github:

https://github.com/sam81/pybdf


Installation
============

Requirements
------------
To install pybdf you will need:
 - python 
 - numpy 
 - a fortran compiler

On all platforms, after having unpacked the archive
you can install pybdf by running::

    python setup.py install

Note that pybdf has been built and tested only on Linux. I don't have
enhough time to build and test binaries for Windows and Mac OS X, but if
you try, please let me know how you get on with it.


*****
Usage
*****

To open a bdf file you need to create a bdfRecording
object as follows::

    bdfRec = bdfRecording('res1.bdf') 

you can then query the properties of the recording stored in the BDF header using the
appropriate functions, which are fully described :ref:`here <module-label>`.
Some examples are shown below.

Get the duration of the recording::

    bdfRec.recordDuration 

Get the sampling rate of each channel::

    bdfRec.sampRate 

Get the channel labels::

    bdfRec.chanLabels

To read in the data use the following method::
  
    rec = bdfRec.getData()

this returns a python dictionary
with the following fields:
- data : an array of floats with dimensions nChannels X nDataPoints
- trigChan : an array of integers with the triggers in decimal format
- statusChan : an array of integers with the status codes in decimal format
For example, to get the value of the first sample of the recording,
in the first channel, you can type::
  rec['data'][0,0]

the same sample value, but for the second channel, is stored in::
  
    rec['data'][1,0]

trigChan contains the triggers for the experimental conditions, in decimal
format. The statusChan, on the other hand, contains system codes, like
cm in/out-of range, battery low/OK. 

Other usage examples are provided in the 'examples' directory inside
the pybdf source archive.

Beware that pybdf does not check that you have sufficient RAM to 
read all the data in a bdf file. If you try to read a file that is
too big for your hardware, you system may become slow or unresponsive.
Initially try reading only a small amount of data, and check how much
RAM that uses. You can read only a portion of the data by passing the
beginning and end arguments to the getData() 
functions. For example, to read the first 10 seconds of the recording, use::
    rec = bdfRec.getData(beginning=0, end=10) 

*****
Bugs
*****

Please, report any bugs on github https://github.com/sam81/pybdf/issues

Known issues
-------------
None


.. _module-label:

***********************************************
:mod:`pybdf` -- Class to read BIOSEMI BDF files
***********************************************

.. automodule:: pybdf
    :members:
