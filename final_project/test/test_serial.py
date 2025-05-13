import serial

with serial.Serial('/dev/ttyUSB0', 115200, timeout=1) as ser:  # Replace COM4 with your actual port
    while True:
        line = ser.readline().decode('utf-8', errors='ignore').strip()
        if line:
            print(line)