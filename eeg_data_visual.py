#/bin/python3.6
'''
Visualization module of the EEG Processing Suite
'''
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.collections import LineCollection

#####
# Plots raw EEG data
# Parameters:
# [eldata] - Raw EEG data in shape n_samples*n_electrodes
# [n_electrodes] - Number of electrodes to be displayed
def plot_eeg_data(eldata, n_electrodes = 2):
    fig = plt.figure("EEG Data")
    ax2 = fig.add_subplot(111)

    t = np.arange(len(eldata)) / 256

    dmin = -512
    dmax = 512
    dr = (dmax - dmin)
    y0 = dmin
    y1 = (n_electrodes - 1) * dr + dmax
    ax2.set_ylim(y0, y1)
    ax2.set_xlim(0, np.max(t))

    ticklocs = []
    segs = []
    for i in range(n_electrodes):
        segs.append(np.hstack((t[:, np.newaxis], eldata[:, i, np.newaxis])))
        ticklocs.append(i * dr)

    offsets = np.zeros((n_electrodes, 2), dtype=float)
    offsets[:, 1] = ticklocs

    lines = LineCollection(segs, offsets=offsets, transOffset=None)
    ax2.add_collection(lines)

    # Set the yticks to use axes coordinates on the y axis
    ax2.set_yticks(ticklocs)
    ax2.set_yticklabels(['E1', 'E2', 'E3', 'E4','E5','E6'])

    ax2.set_xlabel('Time (s)')


    plt.tight_layout()
    plt.show()
 
#####
# Plots  the frequency power specrogram for a given electrode power histogram
# For color intensity, log of the power is used
# [hist] - Histogram data produced by eeg_data.process.eeg_raw_to_hist()
# [elid] - ID of the elctrode to be used for plotting
# [freqs=None] - Frequency index eeg_data.process.eeg_raw_to_hist()
# [colormap="jet"] - Colormap to be used
# [vmin=None] - Value of log hist which is used for the lowest color
#               Default is np.min(log_hist)+0.3*np.ptp(log_hist)
# [vmax=None] - Value of log hist which is used for the higest color
#               Default is np.max(log_hist)
def plot_eeg_log_hist(hist, elid, freqs=None, colormap="inferno",vmin=None,vmax=None):
    log_hist=np.log(hist[elid,:,:])
    if vmin is None:
        vmin = np.min(log_hist)+0.3*np.ptp(log_hist)
    if vmax is None:
        vmax = np.max(log_hist)
    plt.figure(figsize=(15, 7.5))
    ticks = np.arange(0,len(freqs),np.argmax(freqs>5)-1)
    ticklabels = ["{:6.2f}".format(i) for i in freqs[ticks]]
    if freqs is not None:
        plt.gca().set_yticks(ticks)
        plt.gca().set_yticklabels(ticklabels)

    plt.imshow(np.transpose(np.log(hist[elid,:,:])), origin="lower", aspect="auto", cmap=colormap, interpolation="none",vmin=vmin,vmax=vmax)
    plt.xlabel("Time (s)")
    plt.ylabel("Frequency (Hz)")
    plt.title("EEG Spectrogram")
    plt.show()
