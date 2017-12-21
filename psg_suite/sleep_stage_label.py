"""
Contains class for determing and storing sleep stage label data
"""
import numpy as np
import matplotlib.pyplot as plt
from matplotlib import gridspec
from matplotlib.widgets import Slider, Button, RadioButtons
from matplotlib.collections import LineCollection
from matplotlib.colors import LinearSegmentedColormap

class SleepStageLabel():
    """
    Class for determing and storing sleep stage label data
    """
    name = None
    sleep_block = None
    sleep_length = None
    datae = None
    stage_times = None
    stage_labels = None

    def __init__(self, name, date, sleep_block, sleep_length):
        """
        Initializes the stage label

        args:
            name: Name of the recording (usually filename)
            date: Date of the recording
            sleep_block: Identifier for the sleepblock in the recoring (use c1,c2,... for cores  and n1,n2,... for naps)
            sleep_length: Length of the sleep block in seconds
        """
        self.name = name
        self.date = date
        self.sleep_block = sleep_block
        self.sleep_length = sleep_length

    def label_manual(self, display_elems, figsize=(15, 7.5), block=True):
        """
        Displays dialog for manual stage labeling

        args:
            displa_elems: list of lists of parameters used for display in format 
                          ((data_struct,{'parname1':parval1,'parname2':parval2,...}),...)
                          where data_struct is of class containing plot method (such 
                          as EEGSpectralData) and 'parname1':parval1,... are
                          name-value pairs supplied to the function.
            figsize: Size of the figure
            block: Blocks code execution until label dialog is closed
        """
        sleep_stage_labels = ['NREM3','NREM2','REM','NREM1','WAKE','MASK OFF','???']

        height_ratios = np.ones(len(display_elems))*3;
        height_ratios = np.append(height_ratios,1)
        fig=plt.figure(figsize=figsize)
        plt.title("EEG Spectrogram")
        gs = gridspec.GridSpec(len(display_elems)+1, 1, height_ratios=height_ratios)
        ax_transforms = {}
        def on_pick(event):
            print(event.artist)
            if event.artist is None:
                return
            xmouse, ymouse = event.mouseevent.xdata, event.mouseevent.ydata
            xmouse = ax_transforms[event.artist].index_to_time(xmouse)
            #print('x, y of mouse: {:.2f},{:.2f}'.format(xmouse, ymouse))
            larger=[x[0] for x in enumerate(self.stage_times) if x[1] > xmouse]
            if len(larger)>0:
                idx = larger[0]
                if self.stage_labels[idx-1] != self.stage_label:
                    self.stage_times[idx] = xmouse
                    self.stage_labels[idx] = self.stage_label
                else:
                    self.stage_times.pop(idx)
                    self.stage_labels.pop(idx)
            else:
                if self.stage_labels[-1] != self.stage_label:
                    self.stage_times.append(xmouse)
                    self.stage_labels.append(self.stage_label)
            #print(stage_times)
            #print(stage_labels)
            line1.set_xdata(np.concatenate((self.stage_times, [self.sleep_length])))
            line1.set_ydata(np.concatenate((self.stage_labels, [self.stage_labels[-1]])))
            fig.canvas.draw()
            for i in range(1, len(self.stage_labels)):
                if self.stage_labels[i] == self.stage_labels[i-1]:
                    self.stage_labels.pop(i)
                    self.stage_times.pop(i)

        
        for delem in display_elems:
            ax = plt.subplot(gs[0])
            ax_transforms[ax] = delem[0]
            delem[0].plot(axes=ax)
            #TODO
            ax.set_picker(True)
            

            fig.canvas.mpl_connect('pick_event', on_pick)
            fig.set_picker(on_pick)

        xtickspacing = 300;
        if len(np.arange(0,self.sleep_length,300)) > 20:
            xtickspacing = 600;
        if len(np.arange(0,self.sleep_length,600)) > 20:
            xtickspacing = 1200;
        if len(np.arange(0,self.sleep_length,1200)) > 20:
            xtickspacing = 1800;
        if len(np.arange(0,self.sleep_length,1800)) > 20:
            xtickspacing = 3600;
        xticks = np.arange(0,self.sleep_length,xtickspacing)
        xticklabels = [str(int(i/60)) for i in xticks]


        self.stage_times = [0]
        self.stage_labels = [5]
        ax1 = plt.subplot(gs[1])
        line1,=ax1.plot(np.concatenate((self.stage_times,[self.sleep_length])), 
                        np.concatenate((self.stage_labels,[self.stage_labels[-1]])),drawstyle="steps-post")
        ax1.set_xlabel("Time (min)")
        ax1.set_ylabel("Sleep Stage")
        ax1.set_xlim(0,self.sleep_length)
        ax1.set_yticks(np.arange(7))
        ax1.set_yticklabels(sleep_stage_labels)
        ax1.set_xticks(xticks)
        ax1.set_xticklabels(xticklabels)

        self.stage_label = 0
        rax = plt.axes([0.0, 0.0, 0.10, 0.21], facecolor='lightgoldenrodyellow')
        radio = RadioButtons(rax, sleep_stage_labels[::-1], active=self.stage_label)
        axdone = plt.axes([0.9, 0.0, 0.1, 0.075])
        bdone = Button(axdone, 'Next')
        def stagepicker(label):
            self.stage_label = sleep_stage_labels.index(label)
            #print(plot_eeg_log_hist.stage_label)
            #fig.canvas.draw_idle()
        def done(event):
            plt.close()
        bdone.on_clicked(done)
        radio.on_clicked(stagepicker)
        fig.canvas.callbacks.connect('pick_event', on_pick)

        plt.subplots_adjust(left=0.075, bottom=0.25, right=0.99, top=0.99)
        if block:
            plt.show()
        else:
            plt.draw()
        self.stage_times = np.array(self.stage_times)
        self.stage_times = np.concatenate((self.stage_times, [self.sleep_length]))
        self.stage_labels = np.concatenate((self.stage_labels, [6]))







