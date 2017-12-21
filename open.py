#!/bin/python3.6
import numpy as np
import csv
import math
import tkinter
import tkinter.filedialog
import sys
import os

from psg_suite.eeg_data import EEGData
from psg_suite.eeg_spectrum import EEGSpectralData
from psg_suite.sleep_stage_label import SleepStageLabel

def mf():
    if len(sys.argv) > 1:
        fname = sys.argv[1]
    else:
        root_window = tkinter.Tk()
        root_window.withdraw()
        fname = tkinter.filedialog.askopenfilename(filetypes=[('All Supported Files (*.CSV, *.OVIBE, *.DAT)',('.csv','.ovibe','.dat')),('OpenVIBE CSV (*.CSV, *.OPENVIBE)',('.csv','.openvibe')),('Raw (*.DAT)','.dat'),('All Files (*.*)','.*')])
        root_window.destroy()
    if fname == "":
        print("No file was selected - aborting")
        return
    print("---------------------------------------------------------")
    data = EEGData()
    if fname.lower().endswith(".csv") or fname.lower().endswith(".ovibe"):
        print("Loading OpenVIBE capture data from: " + fname + " ...")
        data.load_openvibe(fname)
    elif fname.lower().endswith(".dat"):
        print("Loading raw capture data from: " + fname + " ...")
        data.load_raw(fname)
    else:
        print("Unknown capture format!")
        return
    print(data.data)
    length = len(data.data)
    print("---------------------------------------------------------")
    minutes = int(math.ceil(data.sleep_duration()/60))
    print("data size: " + str(length) + " (" + str(minutes) + " minutes)")
    print("data shape: " + str(np.shape(data)))
    #eeg_data_visual.plot_eeg_data(data)
    spectrum = EEGSpectralData(data)
    print("hist shape: " + str(np.shape(spectrum.data)))
    print("freqs shape: " + str(np.shape(spectrum.frequencystamps)))
    print("max: " + str(np.max(np.log(spectrum.data))))
    print("min: " + str(np.min(np.log(spectrum.data))))
    print("ptp: " + str(np.ptp(np.log(spectrum.data))))
    print("---------------------------------------------------------")
    print("Displaying spectrograms ...")
    figwidth = 7 if minutes < 40 else 16 # adjust figure size based on number of minutes in data set so that naps get a smaller display thats easier to read
    title = os.path.basename(fname).rsplit('.', 1)[0]
    spectrum.frequency_cutoff(25)


    sleep_labels = SleepStageLabel(title,"2017-12-21","C1",data.sleep_duration())
    spectrum.plot(elid=0,figsize=(figwidth,3.3),title=title)
    spectrum.plot(elid=1,figsize=(figwidth,3.3),title=title)
    sleep_labels.label_manual(((spectrum,{"elid":1,'colormap':'parula'}),),title=title,figsize=(figwidth, 3.3))

    print("Saving stage data ...")
    sleep_labels.save_txt(fname+'.stages')
    print("Done")
if __name__ == '__main__':
    mf()
