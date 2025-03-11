import socket
import time

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(('0.0.0.0', 8080))
server.listen(4096)

print("Server listening on port 8080...")

while True:
    conn, addr = server.accept()
    print(f"Connection received from {addr}")
    conn.sendall(b"Hello, you are connected!\n")
    conn.close()
