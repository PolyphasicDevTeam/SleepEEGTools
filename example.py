#!/bin/python3.6
import numpy as np
import eeg_data_io
import eeg_data_visual
import eeg_data_process
data = eeg_data_io.load_eeg_raw('sample_data/out_2017-09-30_n6.dat')
print(data)
#eeg_data_visual.plot_eeg_data(data)
hist,freqs = eeg_data_process.eeg_raw_to_hist(data)
print(hist)
print(freqs)
print(hist.shape)
print(np.max(hist))
print(np.min(hist))
hist,freqs = eeg_data_process.eeg_hist_freq_cutoff(hist,freqs,cutoff=40)
eeg_data_visual.plot_eeg_hist(hist,0,freqs)
