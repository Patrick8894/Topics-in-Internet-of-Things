import socket
import json
import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from picar import control, getCarInfo

HOST = "172.20.10.3" # IP address of your Raspberry PI
PORT = 65432          # Port to listen on (non-privileged ports are > 1023)

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    s.bind((HOST, PORT))
    s.listen()
    try:
        while True:
            client, clientInfo = s.accept()
            print("server recv from: ", clientInfo)
            try:
                while True:
                    data = client.recv(1024)  # receive 1024 Bytes of message in binary format
                    if not data:
                        break  # Client closed the connection
                    print(data)
                    if data == b"getCarInfo":
                        car_info = getCarInfo()
                        car_info_json = json.dumps(car_info)
                        client.sendall(car_info_json.encode('utf-8'))
                    else :
                        message = data.decode('utf-8')
                        control(message)
            except Exception as e:
                print(f"Exception: {e}")
            finally:
                print("Closing client socket")
                client.close()
                control("stop")
    except KeyboardInterrupt:
        print("Server shutting down")
    except Exception as e:
        print(f"Exception: {e}")
    finally:
        print("Closing server socket")
        s.close()   