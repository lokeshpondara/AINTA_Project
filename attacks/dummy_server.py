import socket

server = socket.socket()
server.bind(("0.0.0.0", 9999))
server.listen(5)

print("Dummy server running on port 9999...")

while True:
    client, addr = server.accept()
    print(f"Connection from {addr}")
    client.send(b"Hello from dummy server!")
    client.close()