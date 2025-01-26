#filtret for baseline støj 
# Importer nødvendige biblioteker
import matplotlib.pyplot as plt
import numpy as np
from scipy.signal import butter, sosfilt
import wfdb

# Attributter
Ts = 1 / 500  # Samplingperiode (sekunder)
Fs = 1 / Ts   # Samplingfrekvens (Hz)
N = 2000      # Antal samples
t = np.arange(0, N * Ts, Ts)  # Tidsvektor

# Læs EKG-data ved hjælp af wfdb (rå og filtrerede signaler)
signals1, info = wfdb.rdsamp('rec_6', channels=[0, 1], sampfrom=0, sampto=N)
ecg0 = signals1[:, 0]  # Rå EKG-data (med baseline wander)

# Design et højpasfilter for at fjerne baseline wander
sos = butter(4, 0.5, btype='highpass', fs=Fs, output='sos')  # 0.5 Hz cut-off frekvens
filtered_ecg = sosfilt(sos, ecg0)  # Anvend filteret på det rå signal

# Visualisering af det filtrerede signal
plt.figure(figsize=(10, 5))
plt.plot(t, filtered_ecg, label="Filtreret EKG", color="green")
plt.title("Filtreret EKG Signal i Tidsdomænet")
plt.xlabel("Tid (s)")
plt.ylabel("Amplitude (mV)")
plt.legend()
plt.grid(True)
plt.show()