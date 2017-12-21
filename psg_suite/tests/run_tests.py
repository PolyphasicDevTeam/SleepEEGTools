#!/usr/bin/python3

import unittest
import sys
sys.path.append("..")
import eeg_data

class EEGDataTest(unittest.TestCase):

    def test_load_raw(self):
        d = eeg_data.EEGData()
        d.load_raw('data/recording.dat')
        self.assertEqual(d.bitrate,10)
        self.assertEqual(d.n_electrodes,2)
        self.assertEqual(d.sampling_rate,256)
        self.assertEqual(d.origin,512)
        self.assertEqual(d.standartized,False)
        self.assertEqual(d.data[0,0],528.0)
        self.assertEqual(d.data[0,1],534.0)
        self.assertEqual(d.data[-1,0],519.0)
        self.assertEqual(d.data[-1,1],513.0)
        self.assertEqual(d.data.shape,(432676, 2))

    def test_repickle(self):
        d = eeg_data.EEGData()
        d.load_raw('data/recording.dat')
        d.save_pkl('data/recording.dat.pkl')
        l = eeg_data.EEGData()
        l.load_pkl('data/recording.dat.pkl')
        self.assertEqual(l.bitrate,d.bitrate)
        self.assertEqual(l.n_electrodes,d.n_electrodes)
        self.assertEqual(l.sampling_rate,d.sampling_rate)
        self.assertEqual(l.origin,d.origin)
        self.assertEqual(l.standartized,d.standartized)
        self.assertEqual(l.data.all(),d.data.all())


if __name__ == '__main__':
    unittest.main()
