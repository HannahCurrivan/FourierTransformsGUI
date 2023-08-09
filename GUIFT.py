# Packages required for this script.
from scipy.fft import fft, fftfreq
import matplotlib.pyplot as plt
import numpy as np
import PySimpleGUI as sg

#GUI information      
sg.theme('DarkBlue14')

#Entering the data
tab1_layout = [
    [sg.Text('Sample Rate (Hertz)', size =(45, 1))],
    [sg.Slider((0,50000), orientation='h', s=(10,15), key = '-SR-')],
    [sg.Text('Duration (Seconds)', size =(32, 1))],
    [sg.Slider((0,60), orientation='h', s=(10,15), key = '-DR-')],
    [sg.Text('Calculated Outcome and Graph', size =(26, 1))],
    [sg.Button('Calculate'), sg.Button('Exit')]] 
 
window = sg.Window('Fourier Series', tab1_layout) 

while True:
    event, values = window.read()
    if event in (None, 'Exit'):
        break
    if event == 'Calculate':
        SAMPLE_RATE = int(values['-SR-'])  # Hertz
        DURATION = int(values['-DR-'])  # Seconds
        
        def gen_sine_wave(freq, sr, dur):
            x = np.linspace(0, dur, sr * dur, endpoint=False)
            frequencies = x * freq
            y = np.sin((2 * np.pi) * frequencies)# 2pi because np.sin takes radians
            return x, y
        
        _, nice_tone = gen_sine_wave(250, SAMPLE_RATE, DURATION)
        _, noise_tone = gen_sine_wave(3000, SAMPLE_RATE, DURATION)
        noise_tone = noise_tone * 0.3
        
        mixed_tone = nice_tone + noise_tone
        normalized_tone = np.int16((mixed_tone / mixed_tone.max()) * 32767)
        
        # Number of samples in normalised tone
        N = SAMPLE_RATE * DURATION
        
        yf = fft(normalized_tone)
        xf = fftfreq(N, 1 / SAMPLE_RATE)
        
        # Generate a 6 hertz sine wave that lasts for 5 seconds
        x, y = gen_sine_wave(3, SAMPLE_RATE, DURATION)
        
        plt.figure()
        plt.plot(x, y)
        plt.title('x-coordinates of the sine wave ')
        plt.show()
        
        
        plt.figure()
        plt.plot(normalized_tone[:1000])
        plt.title('Mixed tone')
        plt.show()
        
        plt.figure()
        plt.plot(xf, np.abs(yf))
        plt.title('Frequency over the normalised tone')
        plt.show()

window.close()
