import serial
import csv
import time

PORT = 'COM3'           # Replace with your ESP32's port!
BAUD_RATE = 115200
FILENAME = 'imu_data.csv'
DURATION = 30           # seconds

ser = serial.Serial(PORT, BAUD_RATE, timeout=1)
time.sleep(2)  # Let ESP32 reset

with open(FILENAME, 'w', newline='') as file:
    writer = csv.writer(file)
    writer.writerow(['Time(ms)', 'aX', 'aY', 'aZ', 'gX', 'gY', 'gZ'])

    print(f"Logging for {DURATION} seconds...")
    start_time = time.time()

    while True:
        try:
            line = ser.readline().decode('utf-8').strip()
            if line:
                data = line.split(',')
                if len(data) == 7:
                    writer.writerow(data)
                    print(data)
            if time.time() - start_time > DURATION:
                print(f"\nDone. Data saved to '{FILENAME}'")
                break
        except Exception as e:
            print("Error:", e)
            break

ser.close()
