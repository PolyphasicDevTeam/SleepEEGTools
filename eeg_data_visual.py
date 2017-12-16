#/bin/python3.6
'''
Visualization module of the EEG Processing Suite
'''
import numpy as np
import matplotlib.pyplot as plt
from matplotlib import gridspec
from matplotlib.widgets import Slider, Button, RadioButtons
from matplotlib.collections import LineCollection
from matplotlib.colors import LinearSegmentedColormap

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
# [colormap="parula"] - Colormap to be used
# [spacing=1792] - Spacing used when generating the histogram
# [vmin=None] - Value of log hist which is used for the lowest color
#               Default is np.min(log_hist)+0.3*np.ptp(log_hist)
# [vmax=None] - Value of log hist which is used for the higest color
#               Default is np.max(log_hist)
# [label=1] - 1=Labeling mode On, 0=Off
def plot_eeg_log_hist(hist, elid, freqs=None, colormap="parula",spacing=1792,vmin=None,vmax=None,label=True):
    log_hist=np.log(hist[elid,:,:])
    sleep_dur = np.shape(log_hist)[0]*spacing/256
    if vmin is None:
        vmin = np.min(log_hist)+0.5*np.ptp(log_hist)
    if vmax is None:
        vmax = np.max(log_hist)
    if colormap == "parula":
        global parula_map
        colormap = parula_map
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
    xticks = xticks/(1792/256)
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
        line1,=ax1.plot(np.concatenate((stage_times,[sleep_dur/(spacing/256)])), np.concatenate((stage_labels,[stage_labels[-1]])),drawstyle="steps-post")
        ax1.set_xlabel("Time (min)")
        ax1.set_ylabel("Sleep Stage")
        ax1.set_xlim(0,sleep_dur/(spacing/256))
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
            line1.set_xdata(np.concatenate((stage_times,[sleep_dur/(spacing/256)])))
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
    plt.subplots_adjust(left=0.075, bottom=0.14, right=0.99, top=0.99)
    plt.show()
    stage_times = np.array(stage_times)*(spacing/256)
    if label:
        return stage_times, stage_labels
    else:
        return None



parula_cm_data = [[0.2081, 0.1663, 0.5292], [0.2116238095, 0.1897809524, 0.5776761905], 
    [0.212252381, 0.2137714286, 0.6269714286], [0.2081, 0.2386, 0.6770857143], 
    [0.1959047619, 0.2644571429, 0.7279], [0.1707285714, 0.2919380952, 
    0.779247619], [0.1252714286, 0.3242428571, 0.8302714286], 
    [0.0591333333, 0.3598333333, 0.8683333333], [0.0116952381, 0.3875095238, 
    0.8819571429], [0.0059571429, 0.4086142857, 0.8828428571], 
    [0.0165142857, 0.4266, 0.8786333333], [0.032852381, 0.4430428571, 
    0.8719571429], [0.0498142857, 0.4585714286, 0.8640571429], 
    [0.0629333333, 0.4736904762, 0.8554380952], [0.0722666667, 0.4886666667, 
    0.8467], [0.0779428571, 0.5039857143, 0.8383714286], 
    [0.079347619, 0.5200238095, 0.8311809524], [0.0749428571, 0.5375428571, 
    0.8262714286], [0.0640571429, 0.5569857143, 0.8239571429], 
    [0.0487714286, 0.5772238095, 0.8228285714], [0.0343428571, 0.5965809524, 
    0.819852381], [0.0265, 0.6137, 0.8135], [0.0238904762, 0.6286619048, 
    0.8037619048], [0.0230904762, 0.6417857143, 0.7912666667], 
    [0.0227714286, 0.6534857143, 0.7767571429], [0.0266619048, 0.6641952381, 
    0.7607190476], [0.0383714286, 0.6742714286, 0.743552381], 
    [0.0589714286, 0.6837571429, 0.7253857143], 
    [0.0843, 0.6928333333, 0.7061666667], [0.1132952381, 0.7015, 0.6858571429], 
    [0.1452714286, 0.7097571429, 0.6646285714], [0.1801333333, 0.7176571429, 
    0.6424333333], [0.2178285714, 0.7250428571, 0.6192619048], 
    [0.2586428571, 0.7317142857, 0.5954285714], [0.3021714286, 0.7376047619, 
    0.5711857143], [0.3481666667, 0.7424333333, 0.5472666667], 
    [0.3952571429, 0.7459, 0.5244428571], [0.4420095238, 0.7480809524, 
    0.5033142857], [0.4871238095, 0.7490619048, 0.4839761905], 
    [0.5300285714, 0.7491142857, 0.4661142857], [0.5708571429, 0.7485190476, 
    0.4493904762], [0.609852381, 0.7473142857, 0.4336857143], 
    [0.6473, 0.7456, 0.4188], [0.6834190476, 0.7434761905, 0.4044333333], 
    [0.7184095238, 0.7411333333, 0.3904761905], 
    [0.7524857143, 0.7384, 0.3768142857], [0.7858428571, 0.7355666667, 
    0.3632714286], [0.8185047619, 0.7327333333, 0.3497904762], 
    [0.8506571429, 0.7299, 0.3360285714], [0.8824333333, 0.7274333333, 0.3217], 
    [0.9139333333, 0.7257857143, 0.3062761905], [0.9449571429, 0.7261142857, 
    0.2886428571], [0.9738952381, 0.7313952381, 0.266647619], 
    [0.9937714286, 0.7454571429, 0.240347619], [0.9990428571, 0.7653142857, 
    0.2164142857], [0.9955333333, 0.7860571429, 0.196652381], 
    [0.988, 0.8066, 0.1793666667], [0.9788571429, 0.8271428571, 0.1633142857], 
    [0.9697, 0.8481380952, 0.147452381], [0.9625857143, 0.8705142857, 0.1309], 
    [0.9588714286, 0.8949, 0.1132428571], [0.9598238095, 0.9218333333, 
    0.0948380952], [0.9661, 0.9514428571, 0.0755333333], 
    [0.9763, 0.9831, 0.0538]]

parula_map = LinearSegmentedColormap.from_list('parula', parula_cm_data)
    

