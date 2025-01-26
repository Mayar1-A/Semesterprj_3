#Filteret for powerline støj
import numpy as np
import matplotlib.pyplot as plt
from scipy import signal
import wfdb

# Attributter
fs = 500  # Samplingfrekvens (Hz)
N = 2000  # Antal samples (2 sekunder)
t = np.linspace(0, N / fs, N, endpoint=False)  # Tidsvektor

# Læs EKG-data ved hjælp af wfdb
signals, info = wfdb.rdsamp('rec_12', channels=[0])  # Sørg for, at 'rec_12' er tilgængelig
ecg_signal = signals[:N, 0]  # Rå EKG-data (første kanal)

# Design og anvend et notch-filter
notch_freq = 50  # Frekvensen på støjen (50 Hz)
Q = 30  # Quality factor (smal båndbredde omkring 50 Hz)
b, a = signal.iirnotch(notch_freq, Q, fs)  # Design notch-filter
ecg_filtered = signal.filtfilt(b, a, ecg_signal)  # Filtrer signalet

# Visualisering af kun det filtrerede signal
plt.figure(figsize=(10, 5))
plt.plot(t, ecg_filtered, label="Filtreret EKG", color="red", linewidth=2)
plt.title("Filtreret EKG Signal")
plt.xlabel("Tid (s)")
plt.ylabel("Amplitude (mV)")
plt.legend()
plt.grid(True)
plt.show()
