#Oscilloscope project

import os
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.widgets import Cursor, Button

def data_to_dec(csvfile):
    """
    Function that download data from csv file and then converts them to its decimal representation.
    """
    data = []  # empty list
    if os.path.isfile(csvfile):  # check whether file exists
        with open(csvfile, "r") as content:  # opens file for read
            for line in content:
                line = line.replace("\n", "")  # deletes EOF characters
                line = line.replace("\r", "")  # deletes EOF characters
                line = int(str(line), base=16)
                data.append(line)
    else:
        print(f'Data file {csvfile}, does not exist!')

    return data

#Functions for handling mouse click events

def onclick(event):
    global x1, y1
    print("FIGURE 1 - TIME DOMAIN")
    x1, y1 = event.xdata, event.ydata
    print(f'First coordinates: {x1}, {y1}')

def afterclick(event):
    x2, y2 = event.xdata, event.ydata
    print(f'Second coordinates: {x2}, {y2}')
    print(f'Coordinates differential: {x1-x2}, {y1-y2} \n')

def onclick_f2(event):
    global x3, y3
    print("FIGURE 2 - NYQUIST PLOT")
    x3, y3 = event.xdata, event.ydata
    print(f'First coordinates: {x3}, {y3}')

def afterclick_f2(event):
    x4, y4 = event.xdata, event.ydata
    print(f'Second coordinates: {x4}, {y4}')
    print(f'Coordinates differential: {x3-x4}, {y3-y4} \n')



points_y = np.array(data_to_dec('ADC_data.csv'))

# 10 bit converter - returns values in range of 0 to 1023
points_y=points_y*5/1023

n_samples = len(points_y)
sampling_freq = 900

points_x = np.arange(0,n_samples/sampling_freq, 1/sampling_freq)
fig, ax = plt.subplots()
ax.plot(points_x[:50], points_y[:50])
plt.title('Time domain waveform',fontsize=12)
plt.suptitle('In order to measure coordinates differential click on one point, move to another and realase mouse button',fontsize=8, y=1)
ax.set_xlabel('Time [s]')
ax.set_ylabel('Voltage [V]')
cursor1 = Cursor(ax, useblit=True, color='red', linewidth=2)

fig.canvas.mpl_connect('button_press_event', onclick)
fig.canvas.mpl_connect('button_release_event', afterclick)


np_fft = np.fft.fft(points_y)
amplitudes = 1 / n_samples * np.abs(np_fft)
frequencies = np.fft.fftfreq(n_samples) * n_samples * 1 / (n_samples/sampling_freq)

fig2, ax2 = plt.subplots()
#ax2.semilogx(frequencies[:len(frequencies) // 2], amplitudes[:len(np_fft) // 2])
ax2.plot(frequencies[:len(frequencies)], amplitudes[:len(np_fft)])
plt.title('Nyquist plot',fontsize=12)
plt.suptitle('In order to measure coordinates differential click on one point, move to another and realase mouse button',fontsize=8, y=1)
ax.set_xlabel('Frequency [Hz]')
ax.set_ylabel('Amplitude')
cursor2 = Cursor(ax2, useblit=True, color='red', linewidth=2)
fig2.canvas.mpl_connect('button_press_event', onclick_f2)
fig2.canvas.mpl_connect('button_release_event', afterclick_f2)

plt.show()




