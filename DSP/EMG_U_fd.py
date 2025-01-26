#test_EMG filter_C

import matplotlib.pyplot as plt
import numpy as np
from scipy.signal import butter, sosfilt, filtfilt
import wfdb

# Parametre
Ts = 1 / 500  # Samplingperiode (sekunder)
Fs = 1 / Ts   # Samplingfrekvens (Hz)
N = 2000      # Antal samples
t = np.arange(0, N * Ts, Ts)  # Tidsvektor

# Læs EKG-data ved hjælp af wfdb
signals, info = wfdb.rdsamp('rec_6', channels=[0, 1], sampfrom=0, sampto=N)
ecg0 = signals[:, 0]  # Rå EKG-data 



# DESIGN et MA-filter til EMG-støj
window_size = 10           # Vinduesstørrelse (10 samples = 20 ms)
h = [1/10] * window_size   # 10 ligeligt vægtede samples
#ku også skrives som h = [1/10, 1/10, 1/10, 1/10, 1/10, 1/10, 1/10, 1/10, 1/10, 1/10]

# Anvend MA-filteret på signalet
filtered_ecg = filtfilt(h, [1], ecg0)



#plot i frekvense domæne (rå data)
plt.magnitude_spectrum(ecg0,Fs=Fs)
plt.title('ECG rå med støj')
plt.show()
#print(ecg0-filtretsSignal)

#plot i frekvense domæne (filteret data)
plt.magnitude_spectrum(filtered_ecg,Fs=Fs)
plt.title('filtreret for EMG støj')
plt.show()