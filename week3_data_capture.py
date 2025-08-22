import csv
import time
import random  # Only if simulating sensor data

# Simulate data if no sensor is connected
def get_sensor_data():
    temperature = round(random.uniform(20, 30), 2)
    humidity = round(random.uniform(40, 60), 2)
    return temperature, humidity

# CSV setup
filename = "week3_sensor_data.csv"
with open(filename, mode='w', newline='') as file:
    writer = csv.writer(file)
    writer.writerow(["timestamp", "temperature", "humidity"])  # header

    print("Recording data for 10 minutes...")
    start_time = time.time()
    while time.time() - start_time < 600:  # 600 seconds = 10 minutes
        timestamp = time.strftime("%Y-%m-%d %H:%M:%S")
        temperature, humidity = get_sensor_data()
        writer.writerow([timestamp, temperature, humidity])
        print(timestamp, temperature, humidity)
        time.sleep(2)  # update every 2 seconds
