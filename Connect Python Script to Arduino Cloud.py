# Step 5: Python device connection
from arduino_iot_client import ArduinoDeviceClient
import pandas as pd
import numpy as np
import plotly.express as px
from datetime import datetime
import time

# Initialize connection
device = ArduinoDeviceClient(
    device_id="368de09c-2f11-4045-b7bd-7c9ffc6c5465",
    secret_key="D1f2G3h4J5k6L7m8N9o0P1q2R3s4T5u6"
)

# Lists to store sensor readings
buffer_data = []   # continuous buffer
plot_data = []     # data to plot
N = 1000           # number of samples per graph

def on_x(value):
    buffer_data.append({'timestamp': datetime.now(), 'x': value, 'y': device.get_variable('y'), 'z': device.get_variable('z')})

# Link variables
device.on_message('x', on_x)

print("Receiving accelerometer data...")

while True:
    device.loop()
    if len(buffer_data) >= N:
        # Move N samples to plot_data
        plot_data = buffer_data[:N]
        buffer_data = buffer_data[N:]

        # Create DataFrame
        df = pd.DataFrame(plot_data)

        # Plot and save
        fig = px.line(df, x='timestamp', y=['x','y','z'], title='Accelerometer Readings')
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        fig.write_html(f"plot_{timestamp}.html")
        df.to_csv(f"data_{timestamp}.csv", index=False)

        print(f"Saved graph and data for {timestamp}")
    time.sleep(0.5)
