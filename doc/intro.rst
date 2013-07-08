 
************
Introduction
************
:Author: Samuele Carcagno

pybdf is a Python library to read electroencephalographic 
recordings stored in the BIOSEMI 24-bit BDF format. 


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

Note that pybdf has been built and tested only on Linux with Python3. I don't have
enhough time to build and test binaries for Windows and Mac OS X, but if
you try, please let me know how you get on with it.


*****
Usage
*****

To open a bdf file you need to create a `bdfRecording`
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

- eventTable : a dictionary with the codes, indexes and durations of triggers

- chanLabels : a list with the channel labels

For example, to get the value of the first sample of the recording,
in the first channel, you can type::

    rec['data'][0,0]

the same sample value, but for the second channel, is stored in::
  
    rec['data'][1,0]

The `eventTable` contains a list of the trigger codes for the experimental conditions::

    rec['eventTable`]['code']

as well as a list of the sample numbers (or indexes) at which they started in the recording, and a list of their durations in seconds::

    rec['eventTable']['idx']
    rec['eventTable`]['dur']

The ActiveTwo actually stores one trigger code for each recording sample rather than
a list of trigger onsets and durations as the `eventTable` does. The "raw" trigger channel
with one trigger code for each recording sample can be retrieved by passing the argument `trigChan = True`
to the `getData()` function::

    rec = bdfRec.getData(trigChan=True)

the "raw" trigger channel will then be returned in `rec['trigChan']`.

It is also possible to retrieve additional system codes (bits 16-23 of the
status channel, see http://www.biosemi.com/faq/trigger_signals.htm), like CMS 
in/out-of range, battery low/OK. These are returned in `rec['sysCodeChan']`
when the `sysCodeChan = True` argument is passed to the `getData()` function.
No particular effort has been made to decode these system codes.


Other usage examples are provided in the 'examples' directory inside
the pybdf source archive.

Beware that pybdf does not check that you have sufficient RAM to 
read all the data in a bdf file. If you try to read a file that is
too big for your hardware, you system may become slow or unresponsive.
Initially try reading only a small amount of data, and check how much
RAM that uses. You can read only a portion of the data by passing the
beginning and end arguments to the getData() function. 
For example, to read the first 10 seconds of the recording, use::

    rec = bdfRec.getData(beginning=0, end=10) 

******
Bugs
******

Please, report any bugs on github https://github.com/sam81/pybdf/issues

Known issues
=============

The filename or filepath of the BDF recording is currently limited
to 256 characters. That should be sufficient for most purposes.


.. _module-label:

***********************************************
:mod:`pybdf` -- Class to read BIOSEMI BDF files
***********************************************

.. automodule:: pybdf
    :members:
