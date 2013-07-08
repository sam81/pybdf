#!/usr/bin/env python
# -*- coding: utf-8 -*-

#   Copyright (C) 2012-2013 Samuele Carcagno <sam.carcagno@gmail.com>
#   This file is part of pybdf

#    pybdf is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.

#    pybdf is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.

#    You should have received a copy of the GNU General Public License
#    along with pybdf.  If not, see <http://www.gnu.org/licenses/>.

"""
This module can be used to read the header and data from
24-bit Biosemi BDF files recorded with the ActiveTwo system.

**Examples**

 >>> bdfRec = bdfRecording('res1.bdf') #create bdfRecording object
 >>> bdfRec.recordDuration #how many seconds the recording lasts
 >>> bdfRec.sampRate #sampling rate for each channel
 >>> #read 10 seconds of data from the first two channels
 >>> rec = bdfRec.getData(channels=[0, 1], beginning=0, end=10)
"""
from __future__ import nested_scopes, generators, division, absolute_import, with_statement, print_function, unicode_literals
import copy, numpy
import libforbdf
from numpy import concatenate, diff, where

__version__ = "0.2.2"

class bdfRecording:
    """
    Class for dealing with BIOSEMI 24-bit BDF files.
    A bdfRecording object is created with the following syntax::
        >>> bdfRec = bdfRecording('bdf_file.bdf')
    This reads the BDF header, but not the data. You need to use
    the getData() method to read the data.
    The full documentation of the BDF file format can be found here:
    http://www.biosemi.com/faq/file_format.htm

    Attributes
    ----------
    idCode : str
        Identification code
    subjId : str
        Local subject identification
    recId : str
        Local recording identification
    startDate : str
        Recording start date
    startTime : str
        Recording start time
    nBytes : int
        Number of bytes occupied by the bdf header
    versionDataFormat : str
        Version of data format
    nDataRecords : int
        Number of data records "-1" if unknown
    recordDuration : float
        Duration of a data record, in seconds
    nChannels : int
        Number of channels in data record
    chanLabels : list of str
        Channel labels
    transducer : list of str
        Transducer type
    physDim : str
        Physical dimension of channels
    physMin : list of int
        Physical minimum in units of physical dimension
    physMax : list of int
        Physical maximum in units of physical dimension
    digMin : list of int
        Digital minimum
    digMax : list of int
        Digital maximum
    prefilt : list of str
        Prefiltering
    nSampRec : list of int
        Number of samples in each data record
    reserved : list of str
        Reserved
    scaleFactor : list of floats
        Scaling factor for digital to physical dimension
    sampRate : list of int
        Recording sampling rate
    statusChanIdx : int
        Index of the status channel
    nDataChannels : int
        Number of data channels containing data (rather than trigger codes)
    dataChanLabels : list of str
        Labels of the channels containing data (rather than trigger codes)
                                            
                                            
    """
    
    def __init__(self, fileName):
        self.fileName = fileName
        f = open(self.fileName, "rb")
        #except IOError:
        #    print("Could not open file. Check that that the file name\
        #    is correct")
        #    return
        #python already throws an IOError if the file
        #does not exist, but maybe we should check that
        #the file is indeed of type BDF
        self.idCodeNonASCII = f.read(1)
        self.idCode = bytes.decode(f.read(7), 'ascii')
        self.subjId = bytes.decode(f.read(80), 'ascii')
        self.recId = bytes.decode(f.read(80), 'ascii')
        self.startDate = bytes.decode(f.read(8), 'ascii')
        self.startTime = bytes.decode(f.read(8), 'ascii')
        self.nBytes = int(bytes.decode(f.read(8), 'ascii'))
        self.versionDataFormat = bytes.decode(f.read(44), 'ascii')
        self.nDataRecords = int(bytes.decode(f.read(8), 'ascii'))
        self.recordDuration = float(bytes.decode(f.read(8), 'ascii').strip())
        self.nChannels = int(bytes.decode(f.read(4), 'ascii'))
        self.chanLabels = []
        self.transducer = []
        self.physDim = []
        self.physMin = []
        self.physMax = []
        self.digMin = []
        self.digMax = []
        self.prefilt = []
        self.nSampRec = []
        self.reserved = []
        self.scaleFactor = []
        self.sampRate = []
        
        self.duration = self.recordDuration * self.nDataRecords
        for i in range(self.nChannels):
            self.chanLabels.append(bytes.decode(f.read(16), 'ascii').strip())
        for i in range(self.nChannels):
            self.transducer.append(bytes.decode(f.read(80), 'ascii').strip())
        for i in range(self.nChannels):
            self.physDim.append(bytes.decode(f.read(8), 'ascii').strip())
        for i in range(self.nChannels):
            self.physMin.append(int(bytes.decode(f.read(8), 'ascii')))
        for i in range(self.nChannels):
            self.physMax.append(int(bytes.decode(f.read(8), 'ascii')))
        for i in range(self.nChannels):
            self.digMin.append(int(bytes.decode(f.read(8), 'ascii')))
        for i in range(self.nChannels):
            self.digMax.append(int(bytes.decode(f.read(8), 'ascii')))
        for i in range(self.nChannels):
            self.prefilt.append(bytes.decode(f.read(80), 'ascii').strip())
        for i in range(self.nChannels):
            self.nSampRec.append(int(bytes.decode(f.read(8), 'ascii')))
        for i in range(self.nChannels):
            self.reserved.append(bytes.decode(f.read(32), 'ascii'))
        for i in range(self.nChannels):
            self.scaleFactor.append((self.physMax[i] - self.physMin[i]) / (self.digMax[i] - self.digMin[i]))
        self.statusChanIdx = self.chanLabels.index("Status")
        self.nDataChannels = self.nChannels - 1
        self.dataChanLabels = copy.copy(self.chanLabels)
        self.dataChanLabels.pop()
        self.sampRate = list(numpy.array(numpy.round(numpy.array(self.nSampRec) / self.recordDuration), dtype=numpy.int16))
        f.close()

    def getData(self, beginning=0, end=None, channels=None, eventTable=True, trigChan=False, sysCodeChan=False):

        """
        Read the data from a bdfRecording object

        Parameters
        ----------
        beginning : int
            Start time of data chunk to read (seconds).
        end : int
            End time of data chunk to read (seconds).
        channels : list of integers or strings
            Channels to read. Both channel numbers, or channel names are accepted. Note that channel numbers are indexed starting from *zero*.
        eventTable : boolean
            If True, return the triggers event table
        trigChan : boolean
            If True, return the channel containing the triggers
        sysCodeChan : boolean
            If True, return the channel containing the system codes
 

        Returns
        -------
        rec : a dictionary with the following keys:
           - data : an array of floats with dimenions nChannels X nDataPoints
           - chanLabels : a list containing the labels of the channels that were read,
             in the same order they are inserted in the data matrix
           - trigChannel : an array of integers with the triggers in decimal format
           - sysCodeChannel : an array of integers with the system codes in decimal format
           - eventTable : a dictionary with the following keys
              - code : array of ints
                 The trigger codes
              - idx : array of ints
                 The indexes of the trigger codes
              - dur : array of floats
                 The duration of the triggers in seconds
          
        
        Examples
        --------
        >>> x = bdfRecording('res1.bdf')
        >>> rec = x.getData(channels=[0, 2], beginning=0, end=10)
        """

        if end is None: #read all data
            end = self.nDataRecords
        if channels is None: #read all data channels
            channels = copy.copy(self.dataChanLabels)
        if len(channels) > self.nDataChannels:
            print("Requested channels more than available channels. Exiting")
            return
        for i in range(len(channels)): #if some or all channels were given as labels convert them to indexes
            if isinstance(channels[i], str):
                channels[i] = self.dataChanLabels.index(channels[i])
        channels = sorted(channels)
        chanLabels = []
        for i in range(len(channels)):
            chanLabels.append(self.dataChanLabels[channels[i]])
        nChannelsToRead = len(channels)
        
        f = open(self.fileName, "rb")
        recordsToRead = end - beginning
        data, statchan = libforbdf.read_channels(self.fileName, beginning, end, self.nChannels, self.nSampRec, self.statusChanIdx)
        data = numpy.array(data*self.scaleFactor[0], dtype=numpy.float32)
        trigChannel = statchan[0,:]
        sysCodeChannel = statchan[1,:]
        chanToDel = []
        for c in range(self.nDataChannels):
            if c not in channels:
                chanToDel.append(c)
        if len(chanToDel) > 0:
            data = numpy.delete(data, numpy.array(chanToDel, dtype=numpy.int16), axis=0)
        
        #event table
        evtTab = {}
        if eventTable == True:
            startPoints = concatenate(([0], where(diff(trigChannel) != 0)[0] + 1))
            stopPoints = concatenate((where(diff(trigChannel) != 0)[0], [len(trigChannel)-1]))
            trigDurs = (stopPoints - startPoints)/self.sampRate[0]
            evt = trigChannel[startPoints]
           
            evtTab['code'] = evt
            evtTab['idx'] = startPoints
            evtTab['dur'] = trigDurs
        else:
            evtTab['code'] = None
            evtTab['idx'] = None
            evtTab['dur'] = None
            

        rec = {}
        rec['data'] = data
        if trigChan == True:
            rec['trigChan'] = trigChannel
        else:
            rec['trigChan'] = None
        if sysCodeChan == True:
            rec['sysCodeChan'] = statusChannel
        else:
            rec['sysCodeChan'] = None
        rec['chanLabels'] = chanLabels
        rec['eventTable'] = evtTab
        return rec

