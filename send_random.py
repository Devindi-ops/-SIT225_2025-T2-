import serial
import time
import random
from datetime import datetime

# Set the serial port and baud rate (adjust the COM port if needed)
ser = serial.Serial('COM4', 9600) 

time.sleep(2)  # Wait for Arduino to reset

while True:
    random_number = random.randint(1, 10)
    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    print(f"[{timestamp}] Sending number: {random_number}")
    ser.write(str(random_number).encode())
    time.sleep(10)  # wait before sending again
