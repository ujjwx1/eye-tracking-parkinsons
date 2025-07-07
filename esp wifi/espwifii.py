import socket
import csv
from datetime import datetime

HOST = '0.0.0.0'
PORT = 12345
CSV_FILE = 'accel_data.csv'

# Initialize CSV file with header
with open(CSV_FILE, mode='w', newline='') as file:
    writer = csv.writer(file)
    writer.writerow(['Timestamp', 'aX', 'aY', 'aZ'])

print(f"Logging to {CSV_FILE}")
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((HOST, PORT))
server.listen(1)
print(f"Server listening on {HOST}:{PORT}")

while True:
    conn, addr = server.accept()
    data = conn.recv(1024).decode().strip()
    conn.close()

    if data:
        try:
            ax, ay, az = map(float, data.split(","))
            timestamp = datetime.now().isoformat(timespec='seconds')
            print(f"[{timestamp}] aX: {ax}, aY: {ay}, aZ: {az}")

            # Append to CSV
            with open(CSV_FILE, mode='a', newline='') as file:
                writer = csv.writer(file)
                writer.writerow([timestamp, ax, ay, az])

        except Exception as e:
            print("Invalid data:", data)