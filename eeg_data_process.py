#!/bin/python
import numpy as np
import collections
from  spectrum import *
import matplotlib.pyplot as plt

def eeg_raw_to_hist(eldata, n_electrodes = 2,window = 4096,step = 256):
    hist = np.zeros((n_electrodes,len(range(window,eldata.shape[0],step)),int(window/2)+1),dtype=np.float)
    for el in range(n_electrodes):
        n = 0;
        for d in range(window,eldata.shape[0],step):
            w = eldata[(d-window):d,el]
            w = w.flatten()
            p = speriodogram(w, detrend=False, sampling=256)
            #plt.plot(p)
            #plt.show()
            hist[el,n,:]=p
            n+=1
    freqs = np.arange(int(window/2)+1)/(int(window/2)) *128
    return hist, freqs

def eeg_hist_freq_cutoff(hist,freqs,cutoff = 45):
    ci = np.argmax(freqs>cutoff)
    hist = hist[:,:,:ci]
    freqs = freqs[:ci]
    return hist,freqs
