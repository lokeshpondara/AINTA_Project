import os

blocked_ips = set()

def block_ip(ip):

    if ip in blocked_ips:
        return

    try:
        print(f"🚫 Blocking IP: {ip}")

        # Windows firewall rule
        os.system(f'netsh advfirewall firewall add rule name="Block_{ip}" dir=in action=block remoteip={ip}')

        blocked_ips.add(ip)

    except Exception as e:
        print("Firewall block failed:", e)