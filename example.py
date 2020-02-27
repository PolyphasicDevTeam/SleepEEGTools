#!/usr/bin/python3.6
import numpy as np
import csv
from psg_suite.eeg_data import EEGData
from psg_suite.eeg_spectrum import EEGSpectralData
from psg_suite.sleep_stage_label import SleepStageLabel
def mf():
    fname = 'sample_data/recording.ovibe'
    data = EEGData()
    data.load_openvibe(fname)
    spectrum = EEGSpectralData(data)
    spectrum.frequency_cutoff(25)
    spectrum.plot()
    sleep_labels = SleepStageLabel("Mono","2017-12-21","C1",data.sleep_duration())
    sleep_labels.label_manual(((spectrum,{"elid":0}),(spectrum,{"elid":1})))
    sleep_labels.save_txt(fname+'.stages')
    print(sleep_labels.stage_times)
    print(sleep_labels.stage_labels)
    sleep_labels.load_txt(fname+'.stages')
    print(sleep_labels.stage_times)
    print(sleep_labels.stage_labels)

if __name__ == '__main__':
    mf()
