import socket
import time

# Server Configuration
HOST = '0.0.0.0'  
PORT = 12345
DELAYED_ACK = False  # Set to True or False based on the test case

# Create Socket
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Enable/Disable Nagle's Algorithm
server_socket.setsockopt(socket.IPPROTO_TCP, socket.TCP_NODELAY, False)

server_socket.bind((HOST, PORT))
server_socket.listen(1)

print(f"Server listening on {HOST}:{PORT}")
conn, addr = server_socket.accept()
print(f"Connection from {addr}")

start_time = time.time()
total_received = 0

with conn:
    while True:
        data = conn.recv(1024)
        if not data:
            break
        total_received += len(data)

end_time = time.time()
print(f"Received {total_received} bytes in {end_time - start_time} seconds")

server_socket.close()
