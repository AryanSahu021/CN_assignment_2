import socket
import time
import random

SERVER_IP = '127.0.0.1'
SERVER_PORT = 8080
NUM_REQUESTS = 1000  # Number of connections to simulate

for i in range(NUM_REQUESTS):
    try:
        client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client.connect((SERVER_IP, SERVER_PORT))  # Connect to server

        message = f"Hello from client {i}"  # Unique message per request
        client.sendall(message.encode())  # Send message
        
        data = client.recv(1024)  # Receive response
        print(f"Received: {data.decode()}")

        client.close()  # Close the connection
    except Exception as e:
        print(f"Error: {e}")

    time.sleep(random.uniform(0.5, 2))  # Random delay between requests
