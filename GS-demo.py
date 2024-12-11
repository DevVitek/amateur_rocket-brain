import serial
from datetime import datetime
import csv

portVar = "/dev/ttyUSB1"

serial = serial.Serial()
serial.baudrate = 1000000
serial.port = portVar
serial.open()

with open("data_log.csv", mode="w", newline="") as csvfile:
    csv_writer = csv.writer(csvfile)
    csv_writer.writerow(["Timestamp", "Value 1", "Value 2", "Value 3", "Value 4", 
                         "Value 5", "Value 6", "Value 7", "Value 8"])

    print("Type 'sc' to begin recording data...")
    while True:
        command = input(">> ").strip().lower()
        if command == "sc":
            print("Collecting data...")
            break
        else:
            print("Waiting for 'sc' command...")

    try:
        while True:
            if serial.in_waiting:
                packet = serial.readline()
                data = packet.decode('utf-8', errors='ignore').rstrip()
                
                # Assuming data comes as a comma-separated string of values
                values = data.split(',')  # Split the incoming data into a list

                # Ensure you only get 8 values (if there are fewer, you can pad with None or leave empty)
                if len(values) == 8:
                    # Create a timestamp for the current reading
                    timestamp = datetime.now().strftime('%H:%M:%S.%f')[:-2]
                    print(f"[{timestamp}] {data}")

                    # Write the timestamp and values to the CSV
                    csv_writer.writerow([timestamp] + values)  # Add timestamp to the list of values
                else:
                    print(f"Received data does not contain 8 values: {data}")

    except KeyboardInterrupt:
        print("\nExiting...")
    finally:
        serial.close()
        print("Disconnected.")


