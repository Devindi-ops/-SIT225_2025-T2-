# save as collect_dht22.py or run in Jupyter notebook cells
import serial
import time
from datetime import datetime
import pandas as pd
import numpy as np
import os
import matplotlib.pyplot as plt
import plotly.express as px

# --------- User settings ----------
SERIAL_PORT = 'COM3'   # change to your serial port, e.g., '/dev/ttyUSB0' on Linux
BAUD_RATE = 115200
OUT_DIR = 'week-2'     # directory to store CSV and plots
FILENAME = 'dht22_data.csv'
SAMPLE_LIMIT = None    # None to run until manual stop; or set number of samples to stop automatically
# ----------------------------------

os.makedirs(OUT_DIR, exist_ok=True)
out_path = os.path.join(OUT_DIR, FILENAME)

# Create file with header if not exists
if not os.path.exists(out_path):
    with open(out_path, 'w') as f:
        f.write('timestamp,temperature,humidity\n')

# Open serial
ser = serial.Serial(SERIAL_PORT, BAUD_RATE, timeout=5)
time.sleep(2)  # wait for Arduino reset

def pc_timestamp():
    return datetime.now().strftime('%Y%m%d%H%M%S')

def clean_value(v):
    try:
        return float(v)
    except:
        return np.nan

sample_count = 0
try:
    print("Starting data collection. Press Ctrl+C to stop.")
    while True:
        line = ser.readline().decode('utf-8').strip()
        if not line:
            continue
        # Expected: DATA,23.45,56.78
        parts = line.split(',')
        if parts[0] == 'DATA' and len(parts) == 3:
            t_raw = parts[1]
            h_raw = parts[2]
            t_val = clean_value(t_raw)
            h_val = clean_value(h_raw)
            ts = pc_timestamp()
            # Append to CSV
            with open(out_path, 'a') as f:
                f.write(f"{ts},{'' if np.isnan(t_val) else format(t_val,'.2f')},{'' if np.isnan(h_val) else format(h_val,'.2f')}\n")
            sample_count += 1
            if SAMPLE_LIMIT and sample_count >= SAMPLE_LIMIT:
                print("Sample limit reached.")
                break
        else:
            # optional: handle ERROR,NaN,NaN or other messages
            print("Serial:", line)
except KeyboardInterrupt:
    print("Stopped by user.")
finally:
    ser.close()
    print(f"Data saved to: {out_path}")

# ---------------------------
# After data collection: load, clean, plot, analyze
# ---------------------------

df = pd.read_csv(out_path, dtype=str)

# Convert timestamp to datetime and numeric columns
df['timestamp'] = pd.to_datetime(df['timestamp'], format='%Y%m%d%H%M%S', errors='coerce')
df['temperature'] = pd.to_numeric(df['temperature'], errors='coerce')
df['humidity'] = pd.to_numeric(df['humidity'], errors='coerce')

# Drop rows where timestamp is NaT
df = df.dropna(subset=['timestamp']).reset_index(drop=True)

# Simple cleaning: interpolate small gaps, drop large gaps
df['temperature'] = df['temperature'].interpolate(limit=5)
df['humidity'] = df['humidity'].interpolate(limit=5)

# Save cleaned version
clean_path = os.path.join(OUT_DIR, 'dht22_data_clean.csv')
df.to_csv(clean_path, index=False)

print("Data summary:")
print(df[['temperature','humidity']].describe())

# Rolling stats (5-minute window example with 10s sampling => 30 samples per 5 min)
window_samples = int(5*60 / 10)
rolling = df[['temperature','humidity']].rolling(window=window_samples, min_periods=1).mean()

# Plot with Plotly
fig = px.line(df, x='timestamp', y=['temperature', 'humidity'], title='DHT22 Temperature & Humidity')
fig.write_html(os.path.join(OUT_DIR, f"dht22_plot_{datetime.now().strftime('%Y%m%d%H%M%S')}.html"))
print("Plot saved as HTML.")

# Matplotlib plot example (for quick PNG)
plt.figure(figsize=(12,6))
plt.plot(df['timestamp'], df['temperature'], label='Temperature (°C)')
plt.plot(df['timestamp'], df['humidity'], label='Humidity (%)')
plt.xlabel('Time')
plt.legend()
plt.tight_layout()
plt.savefig(os.path.join(OUT_DIR, 'dht22_plot.png'))
plt.show()

# Detect spikes (transient events)
temp_resid = df['temperature'] - rolling['temperature']
hum_resid = df['humidity'] - rolling['humidity']
temp_spikes = df[np.abs(temp_resid) > 3*df['temperature'].std()]
hum_spikes = df[np.abs(hum_resid) > 3*df['humidity'].std()]

print("Detected temperature spikes:", len(temp_spikes))
print("Detected humidity spikes:", len(hum_spikes))
