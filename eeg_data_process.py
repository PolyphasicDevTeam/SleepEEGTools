#!/bin/python
'''
Processing module of the EEG Processing suite
'''
import numpy as np
import collections
from  spectrum import *
import matplotlib.pyplot as plt

#####
# Uses raw EEG data to create frequency power distribution histogram
# Prameters:
# [eldata] - Raw EEG data in shape n_sample*n_electrodes
# [window=4096] - N. of samples in sliding window used to estiamte the power at given time point
# [step=256]  - N. of samples between individual power distribution estimations
# Returns
# [hist] - Freq. power distributions for electordes where
#          1st dimension is the electrode
#          2nd dimension is the timepoint
#          3rd dimension is the index of frequency for which the power was computed
# [freqs] - Frequencies which are associated with third dimension of [hist]
# [downsample=1] - Downsamples frequency granularity by said factor (1=no downsampling)
def eeg_raw_to_hist(eldata, n_electrodes = 2,window = 4096,step = 256,downsample=1):
    freqs = np.arange(int(window/2)+1)/(int(window/2)) *128
    freqs = freqs[::downsample]
    hist = np.zeros((n_electrodes,len(range(window,eldata.shape[0],step)),len(freqs)),dtype=np.float)
    for el in range(n_electrodes):
        n = 0;
        for d in range(window,eldata.shape[0],step):
            w = eldata[(d-window):d,el]
            w = w.flatten()
            p = speriodogram(w, detrend=False, sampling=256)
            #plt.plot(p)
            #plt.show()
            hist[el,n,:]=p[::downsample]
            n+=1
    return hist, freqs

#####
# Reduces the histogram data by cutting off frequencies higher than specifed frequency
# Parameters:
# [hist] - Freq. power distribution for electrodes (same as output of eeg_raw_to_hist())
# [freqs] - Frequency index (same as output of eeg_raw_to_hist())
# [cutoff] -  Cutoff freqency above which the histogram data will be removed
# Return:
# [hist] - Same as input but with removed data
# [freqs] - Same as input but with removed data
def eeg_hist_freq_cutoff(hist,freqs,cutoff = 45):
    ci = np.argmax(freqs>cutoff)
    hist = hist[:,:,:ci]
    freqs = freqs[:ci]
    return hist,freqs
