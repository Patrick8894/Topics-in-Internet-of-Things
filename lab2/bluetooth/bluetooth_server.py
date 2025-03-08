import socket
import json
from picar import control, getCarInfo

server_addr = 'D8:3A:DD:9D:A6:07'  # Bluetooth address of your Raspberry Pi
server_port = 1

with socket.socket(socket.AF_BLUETOOTH, socket.SOCK_STREAM, socket.BTPROTO_RFCOMM) as s:
    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    s.bind((server_addr, server_port))
    s.listen(1)
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