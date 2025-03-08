import socket
import msvcrt

server_addr = 'D8:3A:DD:9D:A6:07'
server_port = 1

sock = socket.socket(socket.AF_BLUETOOTH, socket.SOCK_STREAM, socket.BTPROTO_RFCOMM)
sock.connect((server_addr, server_port))

def readkey():
    while True:
        if msvcrt.kbhit():
            return msvcrt.getch().decode('utf-8')

while True:
    key = readkey()
    if key == 'w':
        message = "forward"
    elif key == 'a':
        message = "left"
    elif key == 's':
        message = "backward"
    elif key == 'd':
        message = "right"
    elif key == 's':
        message = "stop"
    elif key == 'i':
        message = "getCarInfo"
    elif key == 'q':
        print("quit")
        break
    else:
        continue

    sock.sendall(message.encode('utf-8'))

    if key == 'i':
        data = sock.recv(1024)
        print('Received', data.decode('utf-8'))

sock.close()