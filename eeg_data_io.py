#!/bin/python
import numpy as np

def load_eeg_raw(fname):
    with open(fname) as f:
        a = f.read().splitlines()

        eldata = np.zeros((len(a),6),dtype=np.float)
        n = 0;
        for ln in a:
            strdata = ln.split(' ')
            eldata[n][0] = float(strdata[0])-512
            eldata[n][1] = float(strdata[1])-512
            eldata[n][2] = float(strdata[2])-512
            eldata[n][3] = float(strdata[3])-512
            eldata[n][4] = float(strdata[4])-512
            eldata[n][5] = float(strdata[5])-512
            n+=1
    return eldata


