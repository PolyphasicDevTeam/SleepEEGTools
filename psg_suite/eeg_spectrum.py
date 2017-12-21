'''
Contains class representing EEG Spectral data
'''
import numpy as np
import collections
from  spectrum import *
import matplotlib.pyplot as plt
from . import plotting_util

class EEGSpectralData():
    """
    Handles computation, manipulation and analysis of 
    EEG spectral data
    """
    timestamps = None
    sapmlestamps = None
    frequencystamps = None
    window = None
    step = None
    n_electrodes = None
    sampling_rate = None
    data = None

    def __init__(self, eegdata, n_electrodes=2, window=2048, step=1792, downsample=1):
        """
        Uses raw EEG data to create frequency power distribution histogram

        Args:
            eegdata: instance of EEGData
            n_electrodes: N. of electrodes to be used for computation
            window: N. of samples in sliding window used to estiamte the power at given time point
            step: N. of samples between individual power distribution estimations
            downsample: Downsampling power in frequency dimension (1=no downsampling)
        """
        self.sampling_rate = eegdata.sampling_rate
        self.step =step
        self.frequencystamps = np.arange(int(window/2)+1)/(int(window/2)) * self.sampling_rate/2
        self.frequencystamps = self.frequencystamps[::downsample]
        self.data = np.zeros((n_electrodes,len(range(window,eegdata.data.shape[0],step)),len(self.frequencystamps)),dtype=np.float)
        for el in range(n_electrodes):
            n = 0;
            for d in range(window,eegdata.data.shape[0],step):
                w = eegdata.data[(d-window):d,el]
                w = w.flatten()
                p = speriodogram(w, detrend=False, sampling=eegdata.sampling_rate)
                self.data[el,n,:]=p[::downsample]
                n+=1
        self.samplestamps = np.arange(window,eegdata.data.shape[0],step);
        self.timestamps = self.samplestamps/self.sampling_rate


    def frequency_cutoff(self,cutoff = 45):
        """
        Reduces the histogram data by cutting off frequencies higher than specifed frequency
        
        Args:
            cutoff: freqency above which the histogram data will be removed
        """
        ci = np.argmax(self.frequencystamps>cutoff)
        self.data = self.data[:,:,:ci]
        self.frequencystamps = self.frequencystamps[:ci]
        
    def plot(self, elid=0, colormap="parula", vmin=None, vmax=None, xlabels=True, axes=None, title="EEG Spectrogram", figsize=(15,7), blocking=False):
        """
        Plots sperctrogram into an axes provided for desired electrode.

        Args:
            elid: Index of the electrode for which spectrogram will be plotted
            colormap: plot colormap (parula by default)
            vmin: Value of log hist which is used for the lowest color, default is np.min(log_hist)+0.43*np.ptp(log_hist)
            vmax: Value of log hist which is used for the higest color, default is np.max(log_hist)-0.03*np.ptp(log_hist)
            xlabels: True to display x axis label, false to hide
            axes: matplotlib.axes.Axes object, None = Make new plot window
            title: Title of the figure when plotting standalone (axes=None)
            figsize: Size of the figure when plotting standalone (axes=None)
            blocking: True to block program execution, false to continue when plotting standalone (axes=None)
        """
        #Log histogram for better visual interpretation
        log_hist=np.log(self.data[elid,:,:])

        #Determine vmin/vmax values
        if vmin is None:
            vmin = np.min(log_hist)+0.43*np.ptp(log_hist)
        if vmax is None:
            vmax = np.max(log_hist)-0.03*np.ptp(log_hist)

        if axes is None:
            fig=plt.figure(figsize=figsize)
            plt.title(title)
            axes = fig.axes[0]

        #Calculate Y axis labels
        yticks = np.arange(0,len(self.frequencystamps), np.argmax(self.frequencystamps>5)-1)
        yticklabels = ["{:6.2f}".format(i) for i in self.frequencystamps[yticks]]

        #Calculate X axis labels
        sleep_dur = self.timestamps[-1]
        xtickspacing = 300;
        if len(np.arange(0,sleep_dur,300)) > 20:
            xtickspacing = 600;
        if len(np.arange(0,sleep_dur,600)) > 20:
            xtickspacing = 1200;
        if len(np.arange(0,sleep_dur,1200)) > 20:
            xtickspacing = 1800;
        if len(np.arange(0,sleep_dur,1800)) > 20:
            xtickspacing = 3600;
        xticks = np.arange(0,sleep_dur,xtickspacing)
        xticklabels = [str(int(i/60)) for i in xticks]
        xticks = xticks/(self.step/self.sampling_rate)

        #Plot the histogram
        axes.set_yticks(yticks)
        axes.set_yticklabels(yticklabels)
        axes.set_xticks(xticks)
        axes.set_xticklabels(xticklabels)
        axes.imshow(np.transpose(log_hist), origin="lower", aspect="auto", 
                cmap=plotting_util.colormap(colormap), interpolation="none",vmin=vmin,vmax=vmax)
        axes.set_ylabel("Frequency (Hz)")
        if xlabels:
            axes.set_xlabel("Time (min)")

        if axes is None:
            if blocking:
                plt.show()
            else:
                plt.draw()


    def index_to_time(self, index):
        """
        Transforms index to time in seconds.

        Args:
            index: histogram array x index

        Returns:
            time: Time associated with provided index in seconds
        """
        return index*self.step/self.sampling_rate
