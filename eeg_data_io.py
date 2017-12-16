#!/bin/python
'''
IO Module of the EEG Processing suite
This package provides means of loading EEG data and converting them to a format which is used
for processing and display in other modules of the EEG Processing suite.
'''
import numpy as np
import warnings

######
#Loads EEG data from a raw, space separated format.
# Prameters:
# [fname] is the name of the file to be loaded
# [n_electrodes=2] can be used to specify number of elecrode traces to read
# Returns: 
# [eldata] 2D array of electrode traces with shape n_samples*n_electrodes
def load_eeg_raw(fname,n_electrodes=2):
    with open(fname) as f:
        a = f.read().splitlines()

        eldata = np.zeros((len(a),n_electrodes),dtype=np.float)
        n = 0;
        for ln in a:
            strdata = ln.split(' ')
            for elid in range(n_electrodes):
                eldata[n][elid] = float(strdata[elid])-512
            n+=1
    return eldata

######
#Loads EEG data from openvibe format.
# Prameters:
# [fname] is the name of the file to be loaded
# [n_electrodes=2] can be used to specify number of elecrode traces to read
# [delim=';'] delimiter used when saving file in OpenVibe
# Returns: 
# [eldata] 2D array of electrode traces with shape n_samples*n_electrodes
def load_eeg_openvibe(fname,n_electrodes=2,delim=';'):
    with open(fname) as f:
        for i, l in enumerate(f):
            pass
    nlines = i
    with open(fname) as f:
        if nlines+1 < 2:
            raise IOError("Invalid file format")
        eldata = np.zeros((nlines,n_electrodes),dtype=np.float)
        n = 0;
        for ln in f:
            ln=ln.rstrip()
            if n == 0:
                print(ln)
                header = ln.split(delim)
                if header[0] != "Time (s)":
                    raise IOError("Invalid file format. First column should be Time.")
                if header[-1] != "Sampling Rate":
                    raise IOError("Invalid file format. Last column should be Sampling Rate.")
                for i in range(1,len(header)-1):
                    if header[i] != "Channel " + str(i):
                        raise IOError("Invalid file format. Column " + str(i+1) +
                            " should be Channel " + str(i))
                if len(header) - 2 < n_electrodes:
                    n_electrodes = len(header) - 2
                    warnings.warn("Not enough electrode channels in the file. Only " 
                            + str(n_electrodes) + " will be read")
                n+=1
                continue
            strdata = ln.split(delim)
            for elid in range(n_electrodes):
                eldata[n-1][elid] = float(strdata[elid+1])-512
            n+=1
    return eldata


