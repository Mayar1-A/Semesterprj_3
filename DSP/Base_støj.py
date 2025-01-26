#Baseline Rådata uden filter 
# Importer nødvendige biblioteker
import matplotlib.pyplot as plt
import numpy as np
import wfdb

# Attributter
Ts = 1 / 500  # Samplingperiode (sekunder)
Fs = 1 / Ts   # Samplingfrekvens (Hz)
N = 2000      # Antal samples
t = np.arange(0, N * Ts, Ts)  # Tidsvektor

# Læs EKG-data ved hjælp af wfdb (rå og filtrerede signaler)
signals1, info = wfdb.rdsamp('rec_6', channels=[0, 1], sampfrom=0, sampto=N)
ecg0 = signals1[:, 0]  # Rå EKG-data (med baseline wander)

# Visualisering af EKG med baseline wander støj
plt.figure(figsize=(10, 5))
plt.plot(t, ecg0, label="Rå EKG med baseline wander", color="blue")
plt.title("ECG med Baseline Wander Støj i Tidsdomænet")
plt.xlabel("Tid (s)")
plt.ylabel("Amplitude (mV)")
plt.legend()
plt.grid(True)
plt.show()