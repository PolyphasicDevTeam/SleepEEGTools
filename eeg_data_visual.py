#/bin/python3.6
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.collections import LineCollection

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

def plot_eeg_hist(hist, elid, freqs=None, colormap="jet"):
    plt.figure(figsize=(15, 7.5))
    ticks = np.arange(0,len(freqs),np.argmax(freqs>5)-1)
    ticklabels = ["{:6.2f}".format(i) for i in freqs[ticks]]
    if freqs is not None:
        plt.gca().set_yticks(ticks)
        plt.gca().set_yticklabels(ticklabels)

    plt.imshow(np.transpose(hist[elid,:,:]), origin="lower", aspect="auto", cmap=colormap, interpolation="none",vmin=0,vmax=10000)
    plt.show()
