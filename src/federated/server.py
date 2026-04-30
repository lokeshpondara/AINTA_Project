import subprocess
import sys

print("Starting Flower server...")
try:
    subprocess.check_call([
        sys.executable, "-m", "flower", "server",
        "--insecure",
        "--host", "localhost",
        "--port", "8080"
    ])
except KeyboardInterrupt:
    print("Server stopped.")


