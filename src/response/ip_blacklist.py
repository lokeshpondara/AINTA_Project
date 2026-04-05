BLACKLIST = set()
BLACKLIST_FILE = "blacklist.txt"


def load_blacklist():
    try:
        with open(BLACKLIST_FILE, "r") as f:
            for line in f:
                BLACKLIST.add(line.strip())
    except FileNotFoundError:
        pass


def save_to_file(ip):
    try:
        with open(BLACKLIST_FILE, "a") as f:
            f.write(ip + "\n")
    except Exception as e:
        print("[ERROR] Failed to save blacklist:", e)


def is_blacklisted(ip):
    return ip in BLACKLIST


def add_to_blacklist(ip):
    if ip not in BLACKLIST:
        BLACKLIST.add(ip)
        save_to_file(ip)
        print(f"🚫 IP {ip} added to blacklist")