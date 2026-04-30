import subprocess
import os

ROOT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../"))

def windows_block_ip(ip, duration_minutes=60):
    """Windows Firewall block IP (Phase 3)"""
    try:
        # Delete existing rule if any
        cmd_delete = f'netsh advfirewall firewall delete rule name="AINTA_BLOCK_{ip}"'
        subprocess.run(cmd_delete, shell=True, capture_output=True)
        
        # Add block rule (inbound/outbound)
        cmd_add = f'''
netsh advfirewall firewall add rule name="AINTA_BLOCK_{ip}" dir=in action=block remoteip={ip} description="AINTA auto-block {duration_minutes}min"
netsh advfirewall firewall add rule name="AINTA_BLOCK_{ip}_out" dir=out action=block remoteip={ip} description="AINTA auto-block {duration_minutes}min"
        '''
        subprocess.run(cmd_add, shell=True, check=True)
        print(f"🔥 Windows Firewall BLOCK {ip} ({duration_minutes}min)")
        return True
    except Exception as e:
        print(f"[ERROR] Windows Firewall block {ip}: {e}")
        return False

def windows_unblock_ip(ip):
    """Remove block rule"""
    cmd = f'netsh advfirewall firewall delete rule name="AINTA_BLOCK_{ip}"'
    subprocess.run(cmd, shell=True, capture_output=True)
    cmd_out = f'netsh advfirewall firewall delete rule name="AINTA_BLOCK_{ip}_out"'
    subprocess.run(cmd_out, shell=True, capture_output=True)
    print(f"✅ Unblocked {ip}")

def is_blocked(ip):
    """Check if IP blocked"""
    cmd = f'netsh advfirewall firewall show rule name="AINTA_BLOCK_{ip}"'
    result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
    return result.returncode == 0
