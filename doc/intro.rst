 
************
Introduction
************
:Author: Samuele Carcagno

pybdf is a pure python library to read BIOSEMI 24-bit BDF files.
While being slower than alternative C-based libraries like
`BioSig <http://biosig.sourceforge.net/>`, it is very easy to install
and use.



*************************
Download and Installation
*************************

Download
========

The latest release of pybdf can be downloaded from the python package index:
 
http://pypi.python.org/pypi/pybdf/

For developers: the source code of pybdf is hosted on
launchpad:

https://launchpad.net/pybdf


Installation
============

Requirements
------------
To install pybdf you will need:
 - python >= 3.2
 - numpy 

On all platforms, after having unpacked the archive
you can install pybdf by running::

    python setup.py install

On Windows, you can alternatively use the binary installer, if provided.
Note that pybdf has not been extensively tested on Windows.

*****
Usage
*****

To open a bdf file you need to create a bdfRecording
object as follows::

    bdf_rec = bdfRecording('res1.bdf') 

you can then query the properties of therecording stored in the BDF header using the
appropriate functions, which are fully described :ref:`here <module-label>`.
Some examples are shown below.

Get the duration of the recording::

    bdf_rec.recordDuration 

Get the sampling rate of each channel::

    bdf_rec.sampRate 

Get the channel labels::

    bdf_rec.chanLabels

There are two functions to read in the data. The first function reads
each channel sequentially::
  rec = bdf_rec.get_data()
the second function reads the channels in parallel, and is thus faster
on multicore machines::
  rec = bdf_rec.get_data_parallel() 

either function returns the same result, that is a python dictionary
with the following fields:
- data : an array of floats with dimenions nChannels X nDataPoints
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

Beware that pybdf does not check that you have sufficeint RAM to 
read all the data in a bdf file. If you try to read a file that is
too big for your hardware, you system may become slow or unresponsive.
Initially try reading only a small amount of data, and check how much
RAM that uses. You can read only a portion of the data by passing the
beginning and end arguments to the get_data() or get_data_parallel()
functions. For example, to read the first 10 seconds of the recording, use::
    rec = bdf_rec.get_data_parallel(beginning=0, end=10) 

*****
Bugs
*****

Please, report any bugs on Launchpad https://launchpad.net/pybdf

Known issues
-------------
Currently there are problems with the get_data_parallel() function 
on Windows. Please, use the get_data() function instead, or use Linux.


**********
Benchmarks
**********

To give you an idea of the speed of pybdf, here are some rough
benchmarks. 

Using the get_data_parallel() function:

========  ============  ============ ========== =============================    =========
Channels  Duration (s)   Samp. Rate   File (MB)  CPU                              Time (s)
========  ============  ============ ========== =============================    =========
   9           931            2048     49.1     Intel Core i7-870                  10

   9           1457           2048     76.8     Intel Core i7-870                  15

   41          651            2048     156.4    Intel Core i7-870                  21

   9           931            2048     49.1     Intel Core2 Quad Q6600             16

   9           1457           2048     76.8     Intel Core2 Quad Q6600             24

   41          651            2048     156.4    Intel Core2 Quad Q6600             31

========  ============  ============ ========== =============================    =========

.. _module-label:

***********************************************
:mod:`pybdf` -- Class to read BIOSEMI BDF files
***********************************************

.. automodule:: pybdf
    :members:
