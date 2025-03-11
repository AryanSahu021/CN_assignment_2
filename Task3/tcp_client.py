import socket
import time

SERVER_IP = '127.0.0.1'  
PORT = 12345
TRANSFER_RATE = 40  # bytes/sec
DELAYED_ACK = False  # Set to True or False based on test case

# Read File
with open("testfile.txt", "rb") as f:
    data = f.read()

# Create Socket
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Enable/Disable Nagle’s Algorithm
client_socket.setsockopt(socket.IPPROTO_TCP, socket.TCP_NODELAY, False)

client_socket.connect((SERVER_IP, PORT))

start_time = time.time()
sent_bytes = 0

# Send data at 40 bytes/sec
for i in range(0, len(data), TRANSFER_RATE):
    chunk = data[i:i+TRANSFER_RATE]
    client_socket.sendall(chunk)
    sent_bytes += len(chunk)
    time.sleep(1)  # Maintain transfer rate

end_time = time.time()
print(f"Sent {sent_bytes} bytes in {end_time - start_time} seconds")

client_socket.close()
