import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import wfdb
import os
UPLOAD_FOLDER = '/home/sugrp005/PythonProject/static/gemt_graf'

def generate_graph():
    # Paths to the files
    file_path = os.path.join(UPLOAD_FOLDER, 'rec_1')  # WFDB expects a base path, not file extensions

    # Check if the required files exist
    dat_file = f"{file_path}.dat"
    hea_file = f"{file_path}.hea"
    if not os.path.exists(dat_file) or not os.path.exists(hea_file):
        print(f"Error: {dat_file} or {hea_file} does not exist.")
        return "Files are missing"

    # Read EKG data
    try:
        signals, info = wfdb.rdsamp('/home/sugrp005/PythonProject/static/gemt_graf/rec_1', channels=[0])
        ecg_signal = signals[:, 0]
    except Exception as e:
        print(f"Error reading WFDB files: {e}")
        return str(e)

    # Generate graph
    plt.figure(figsize=(12, 6))
    plt.plot(ecg_signal, label="EKG Signal", color="green")
    plt.title("EKG Signal")
    plt.xlabel("Time (s)")
    plt.ylabel("Amplitude (mV)")
    plt.legend()
    plt.grid(True)

    # Save the graph
    graph_path = os.path.join(UPLOAD_FOLDER, 'patient_graph.png')
    plt.savefig(graph_path)
    plt.close()
    print(f"Graph saved at: {graph_path}")
    return f"Graph saved at {graph_path}"