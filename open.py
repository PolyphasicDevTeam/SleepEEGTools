#!/bin/python3.6
import numpy as np
import csv
import eeg_data_io
import eeg_data_visual
import eeg_data_process
import math
import tkinter
import sys
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
    if fname.lower().endswith(".csv") or fname.lower().endswith(".ovibe"):
        print("Loading OpenVIBE capture data from: " + fname + " ...")
        data = eeg_data_io.load_eeg_openvibe(fname)
    else:
        print("Loading raw capture data from: " + fname + " ...")
        data = eeg_data_io.load_eeg_raw(fname)
    print(data)
    length = len(data)
    print("---------------------------------------------------------")
    minutes = int(math.ceil(length / 15360))
    print("data size: " + str(length) + " (" + str(minutes) + " minutes)")
    print("data shape: " + str(np.shape(data)))
    #eeg_data_visual.plot_eeg_data(data)
    hist,freqs = eeg_data_process.eeg_raw_to_hist(data)
    print("hist shape: " + str(np.shape(hist)))
    print("freqs shape: " + str(np.shape(freqs)))
    print("max: " + str(np.max(np.log(hist))))
    print("min: " + str(np.min(np.log(hist))))
    print("ptp: " + str(np.ptp(np.log(hist))))
    print("---------------------------------------------------------")
    print("Displaying spectrograms ...")
    figwidth = 7 if minutes < 40 else 16 # adjust figure size based on number of minutes in data set so that naps get a smaller display thats easier to read
    hist,freqs = eeg_data_process.eeg_hist_freq_cutoff(hist,freqs,cutoff=25)
    eeg_data_visual.plot_eeg_log_hist(hist,0,freqs,colormap="parula",figsize=(figwidth, 3.3),label=False,block=False)#,vmin=6,vmax=23
    stimes,slabels=eeg_data_visual.plot_eeg_log_hist(hist,1,freqs,colormap="parula",figsize=(figwidth, 6),label=True,block=True)#,vmin=6,vmax=23
    print("Saving stage data ...")
    wrf = open(fname+'.stages','w')
    wr = csv.writer(wrf)
    for i in range(len(stimes)):
        wr.writerow([stimes[i],slabels[i]])
    wrf.close()
    print("Done")
if __name__ == '__main__':
    mf()