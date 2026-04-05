import socket
import time

target = "127.0.0.1"

ports = [22, 23, 80, 443, 8080, 3306, 21, 25, 110]

print("[+] Starting REAL Port Scan...")

while True:
    for port in ports:
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.settimeout(0.5)
            s.connect((target, port))
            s.close()
        except (socket.timeout, ConnectionRefusedError):
            pass

        print(f"[SCAN] Port {port}")
        time.sleep(0.2)