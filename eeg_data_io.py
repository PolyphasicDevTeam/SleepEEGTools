#!/bin/python
'''
IO Module of the EEG Processing suite
This package provides means of loading EEG data and converting them to a format which is used
for processing and display in other modules of the EEG Processing suite.
'''
import numpy as np

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


