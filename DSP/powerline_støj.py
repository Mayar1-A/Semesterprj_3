import numpy as np
import matplotlib.pyplot as plt
from scipy import signal
import wfdb

# Attributter
fs = 500  # Samplingfrekvens (Hz)
N = 2000  # Antal samples (2 sekunder)
t = np.linspace(0, N / fs, N, endpoint=False)  # Tidsvektor

# Læs EKG-data ved hjælp af wfdb
signals, info = wfdb.rdsamp('rec_12', channels=[0])  # 'rec_12' skal være tilgængelig
ecg_signal = signals[:N, 0]  # Rå EKG-data (første kanal)

# Plot EKG uden tilføjet støj
plt.figure(figsize=(10, 5))
plt.plot(t, ecg_signal, label="Rå EKG Data", color="blue")
plt.title("Rå EKG Data med Powerline Støj")
plt.xlabel("Tid (s)")
plt.ylabel("Millivolts")
plt.legend()
plt.grid(True)
plt.show()
