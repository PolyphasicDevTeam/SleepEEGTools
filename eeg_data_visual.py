#/bin/python3.6
'''
Visualization module of the EEG Processing Suite
'''
import numpy as np
import matplotlib.pyplot as plt
from matplotlib import gridspec
from matplotlib.widgets import Slider, Button, RadioButtons
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
# [label=1] - 1=Labeling mode On, 0=Off
def plot_eeg_log_hist(hist, elid, freqs=None, colormap="inferno",vmin=None,vmax=None,label=True):
    log_hist=np.log(hist[elid,:,:])
    sleep_dur = np.shape(log_hist)[0]
    if vmin is None:
        vmin = np.min(log_hist)+0.3*np.ptp(log_hist)
    if vmax is None:
        vmax = np.max(log_hist)
    fig=plt.figure(figsize=(15, 7.5))
    yticks = np.arange(0,len(freqs),np.argmax(freqs>5)-1)
    yticklabels = ["{:6.2f}".format(i) for i in freqs[yticks]]
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
    plt.gca().set_xticks(xticks)
    plt.gca().set_xticklabels(xticklabels)
    if label is False:
        if freqs is not None:
            plt.gca().set_yticks(yticks)
            plt.gca().set_yticklabels(yticklabels)

        plt.imshow(np.transpose(log_hist), origin="lower", aspect="auto", 
                cmap=colormap, interpolation="none",vmin=vmin,vmax=vmax,picker=label)
        plt.xlabel("Time (min)")
        plt.ylabel("Frequency (Hz)")
        plt.title("EEG Spectrogram")

    if label is True:
        sleep_stage_labels = ['NREM3','NREM2','REM','NREM1','WAKE','MASK OFF','???']
        plt.title("EEG Spectrogram")
        gs = gridspec.GridSpec(2, 1, height_ratios=[3, 1])
        ax0 = plt.subplot(gs[0])
        if freqs is not None:
            ax0.set_yticks(yticks)
            ax0.set_yticklabels(yticklabels)
        ax0.set_xticks(xticks)
        ax0.set_xticklabels(xticklabels)
        ax0.imshow(np.transpose(log_hist), origin="lower", aspect="auto", 
                cmap=colormap, interpolation="none",vmin=vmin,vmax=vmax,picker=label)
        ax0.set_ylabel("Frequency (Hz)")

        stage_times = [0]
        stage_labels = [5]
        ax1 = plt.subplot(gs[1])
        line1,=ax1.plot(np.concatenate((stage_times,[sleep_dur])), np.concatenate((stage_labels,[stage_labels[-1]])),drawstyle="steps-post")
        ax1.set_xlabel("Time (min)")
        ax1.set_ylabel("Sleep Stage")
        ax1.set_xlim(0,sleep_dur)
        ax1.set_yticks(np.arange(7))
        ax1.set_yticklabels(sleep_stage_labels)
        ax1.set_xticks(xticks)
        ax1.set_xticklabels(xticklabels)

        plot_eeg_log_hist.stage_label = 6
        rax = plt.axes([0.0, 0.0, 0.10, 0.10], facecolor='lightgoldenrodyellow')
        radio = RadioButtons(rax, sleep_stage_labels, active=6)
        axdone = plt.axes([0.9, 0.0, 0.1, 0.075])
        bdone = Button(axdone, 'Next')
        def stagepicker(label):
            plot_eeg_log_hist.stage_label = sleep_stage_labels.index(label)
            #print(plot_eeg_log_hist.stage_label)
            #fig.canvas.draw_idle()
        def on_pick(event):
            xmouse, ymouse = event.mouseevent.xdata, event.mouseevent.ydata
            #print('x, y of mouse: {:.2f},{:.2f}'.format(xmouse, ymouse))
            larger=[x[0] for x in enumerate(stage_times) if x[1] > xmouse]
            if len(larger)>0:
                idx = larger[0]
                if stage_labels[idx-1] != plot_eeg_log_hist.stage_label:
                    stage_times[idx] = xmouse
                    stage_labels[idx] = plot_eeg_log_hist.stage_label
                else:
                    stage_times.pop(idx)
                    stage_labels.pop(idx)
            else:
                if stage_labels[-1] != plot_eeg_log_hist.stage_label:
                    stage_times.append(xmouse)
                    stage_labels.append(plot_eeg_log_hist.stage_label)
            #print(stage_times)
            #print(stage_labels)
            line1.set_xdata(np.concatenate((stage_times,[sleep_dur])))
            line1.set_ydata(np.concatenate((stage_labels,[stage_labels[-1]])))
            fig.canvas.draw()
            for i in range(1,len(stage_labels)):
                if stage_labels[i] == stage_labels[i-1]:
                    stage_labels.pop(i)
                    stage_times.pop(i)
        def done(event):
            plt.close()
        bdone.on_clicked(done)
        radio.on_clicked(stagepicker)
        fig.canvas.callbacks.connect('pick_event', on_pick)
    plt.show()
    if label:
        return stage_times, stage_labels
    else:
        return None
