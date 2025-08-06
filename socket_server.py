import socket
import json
from datetime import datetime
from db import save_to_db

HOST = '127.0.0.1'
PORT = 5000
BUFFER_SIZE = 1024

def run_socket_server():
    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as server:
        server.bind((HOST, PORT))
        print(f"Socket Server running at {HOST}:{PORT}")

        while True:
            data, addr = server.recvfrom(BUFFER_SIZE)
            print(f"Received from {addr}: {data}")

            try:
                # Перетворення рядка на словник
                message = eval(data.decode())  # ⚠️ У реальному житті краще використовувати json.loads()
                message["date"] = str(datetime.now())

                # Збереження у MongoDB
                save_to_db(message)

            except Exception as e:
                print(f"Error processing message: {e}")
