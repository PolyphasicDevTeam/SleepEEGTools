#!/bin/python3.6
import numpy as np
import csv
import eeg_data_io
import eeg_data_visual
import eeg_data_process
def mf():
    fname = 'sample_data/record.ovibe'
    data = eeg_data_io.load_eeg_openvibe(fname)

    #fname = 'sample_data/recording.dat'
    #data = eeg_data_io.load_eeg_raw(fname)

    print(data)
    print(np.shape(data))
    #eeg_data_visual.plot_eeg_data(data)
    hist,freqs = eeg_data_process.eeg_raw_to_hist(data)
    print(np.shape(hist))
    print(np.shape(freqs))
    print(np.max(np.log(hist)))
    print(np.min(np.log(hist)))
    print(np.ptp(np.log(hist)))
    hist,freqs = eeg_data_process.eeg_hist_freq_cutoff(hist,freqs,cutoff=40)

    stimes,slabels=eeg_data_visual.plot_eeg_log_hist(hist,0,freqs)

    wrf = open(fname+'.stages','w')
    wr = csv.writer(wrf)
    for i in range(len(stimes)):
        wr.writerow([stimes[i],slabels[i]])
    wrf.close()

if __name__ == '__main__':
    mf()
