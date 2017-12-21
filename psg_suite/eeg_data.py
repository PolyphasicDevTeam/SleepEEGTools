'''
Class for storing EEG Sleep data
'''
import numpy as np
import csv
import warnings
import pickle


'''
Class for storing EEG Sleep data
'''
import numpy as np
class EEGData():
    bitrate = None #Signal in range 0 to 2^bitrate
    n_electrodes = None #Number of electrodes
    sampling_rate = None #Sampling rate of the signal
    origin = None #Number around which the signal is centered, usually 0 or 2^(bitrate-1)
    standartized = None #False = signal range 0 to 2^bitrate, True = s. range -1 to 1
    data = None #Electrodes data
    def __init__(self):
        pass

    def load_raw(self, fname, n_electrodes=2, samp_rate=256,
                 bitrate=10, origin=512, standartized=False):
        """
        Loads EEG data from a raw, space separated format.

        Args:
            fname: Path to file to be loaded
            n_electrodes:  Number of electrode traces to be loaded
            samp_rate: Sampling rate of the recording device
            bitrate: Bitrate of the recording
            origin: Origin around which the signal is centered, usually 0 or 2^(bitrate-1)
            standartized: False = signal range 0 to 2^bitrate, True = s. range -1 to 1
        """
        try:
            with open(fname) as f:
                lines = f.read().splitlines()
                self.data = np.zeros((len(lines),n_electrodes),dtype=np.float)
                n = 0
                for ln in lines:
                    strdata = ln.split(' ')
                    for elid in range(n_electrodes):
                        self.data[n][elid] = float(strdata[elid])
                    n += 1
        except Exception:
            self.data = None
            raise
        self.bitrate = bitrate
        self.n_electrodes = n_electrodes
        self.sampling_rate = samp_rate
        self.origin = origin
        self.standartized = standartized

    def load_openvibe(self, fname, n_electrodes=2, bitrate=10,
                      origin=512, standartized=False, delim=';'):
        """
        Loads EEG data from an OpenVibe file

        Args:
            fname: Path to file to be loaded
            n_electrodes:  Number of electrode traces to be loaded
            bitrate: Bitrate of the recording
            origin: Origin around which the signal is centered, usually 0 or 2^(bitrate-1)
            standartized: False = signal range 0 to 2^bitrate, True = s. range -1 to 1
            delim: Delimiter used to separate entries in the file
        """
        try:
            with open(fname) as f:
                for i, l in enumerate(f):
                    pass
            nlines = i
            with open(fname) as f:
                if nlines+1 < 2:
                    raise IOError("Invalid file format")
                self.data = np.zeros((nlines,n_electrodes),dtype=np.float)
                n = 0;
                for ln in f:
                    ln=ln.rstrip()
                    if n == 0:
                        #print(ln)
                        header = ln.split(delim)
                        if header[0] != "Time (s)":
                            raise IOError("Invalid file format. First column should be Time.")
                        if header[-1] != "Sampling Rate":
                            raise IOError("Invalid file format. Last column "+
                                          "should be Sampling Rate.")
                        for i in range(1, len(header)-1):
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
                    if n == 1:
                        self.sampling_rate = int(strdata[-1])
                    for elid in range(n_electrodes):
                        self.data[n-1][elid] = float(strdata[elid+1])-512
                    n+=1
        except Exception:
            self.data = None
            self.sampling_rate = None
            raise
        self.bitrate = bitrate
        self.n_electrodes = n_electrodes
        self.origin = origin
        self.standartized = standartized

    def load_pkl(self, fname):
        """
        Loads EEG data from pickle file

        Args:
            fname: Path to file to be loaded
        """
        with open(fname,'rb') as f:
            ld = pickle.load(f)
            self.bitrate = ld.bitrate
            self.n_electrodes = ld.n_electrodes
            self.sampling_rate = ld.sampling_rate
            self.origin = ld.origin
            self.standartized = ld.standartized
            self.data = ld.data

    def save_pkl(self, fname):
        """
        Saves EEG data to pickle file

        Args:
            fname: Path to file to be saved
        """
        with open(fname,'wb') as f:
            pickle.dump(self,f)


    def standartize(self):
        """
        Standartizes the data by setting origin to 0 and range to -1 to 1
        """

        if self.standartized:
            return
        self.data = self.data - self.origin
        origin = 0
        self.data = self.data / np.power(2,self.bitrate - 1)
        self.standartized = True

    def sleep_duration(self):
        """
        Returns sleep duration in seconds
        """
        return self.data.shape[0]/self.sampling_rate

