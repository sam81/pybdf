# -*- coding: utf-8 -*-
#!/usr/bin/env python

from __future__ import nested_scopes, generators, division, absolute_import, with_statement, print_function, unicode_literals
import numpy, os, subprocess, time
import pybdf
try:
    import matplotlib.pyplot as plt
    matplotlib_available = True
except:
    matplotlib_available = False

#on linux the following automatically
#downloads example datasets from BIOSEMI
#if you're on windows or mac, download manually
# http://www.biosemi.com/download/BDFtestfiles.zip
#subprocess.call("wget http://www.biosemi.com/download/BDFtestfiles.zip", shell=True)
#subprocess.call("unzip BDFtestfiles.zip", shell=True)
fName1 = "Newtest17-256.bdf"
fName2 = "Newtest17-2048.bdf"
#let's see how long it takes


rec1 = pybdf.bdfRecording(fName1)
data1 = rec1.getData()

rec2 = pybdf.bdfRecording(fName2)
data2 = rec1.getData()

#retrieve sampling rates (list of sampling rate of each channel)
sampRate1 = rec1.sampRate
sampRate2 = rec2.sampRate
print("**********************")
print("The sampling rate of, ", fName1, "is", sampRate1[0], "Hz")
print("The sampling rate of, ", fName2, "is", sampRate2[0], "Hz")
print("--------------\n")

dur1 = rec1.duration
dur2 = rec2.duration
#retrieve recording durations (list of recording durations of each channel)
print("**********************")
print("The duration of, ", fName1, "is", dur1, "seconds")
print("The duration of, ", fName2, "is", dur2, "seconds")

dataMatrix1 = data1['data']
time_array1 = numpy.arange(dataMatrix1.shape[1]) / rec1.sampRate[0]
if matplotlib_available == True:
    fig1 = plt.figure(figsize=(7, 6), dpi=100)
    
    for i in range(2): #plot first 3 channels
        ax = fig1.add_subplot(2,1,i)
        ax.plot(time_array1, dataMatrix1[i,:])
        ax.set_ylabel('Amplitude ($\mu V$)')
        ax.set_xlabel('Time (s)')
    plt.savefig(fName1+".pdf", format='pdf')

#check that there is a 3-Hz signal in the dataset
n = len(dataMatrix1[0])
p = numpy.fft.fft(dataMatrix1[0])
nUniquePts = numpy.ceil((n+1)/2)
p = p[0:nUniquePts]
p = numpy.abs(p)
p = p / n
p = p**2
if n % 2 > 0: # we've got odd number of points fft
    p[1:len(p)] = p[1:len(p)] * 2
else:
    p[1:len(p) -1] = p[1:len(p) - 1] * 2 # we've got even number of points fft
freqArray = numpy.arange(0, nUniquePts, 1) * (rec1.sampRate[0] / n)
if matplotlib_available == True:
    fig1 = plt.figure(figsize=(7, 6), dpi=100)
    ax = fig1.add_subplot(1,1,1)
    ax.plot(freqArray, 10*numpy.log10(p), color='k')
    ax.axvline(x=3, color='r', linestyle=':', linewidth=0.2)
    ax.set_ylabel('Level (dB re. 1$\mu V$)')
    ax.set_xlabel('Frequency (Hz)')
    plt.savefig(fName1+"_fft.pdf", format='pdf')
