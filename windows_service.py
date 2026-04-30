#!/usr/bin/env python
"""
AINTA Windows Service Wrapper (Phase 3)
Requires NSSM: https://nssm.cc/download
"""

import sys
import os
import subprocess
import argparse

SERVICE_NAME = "AINTA_SOC"
SCRIPT_PATH = os.path.abspath("run_system.py")

def install_service():
    """Install as Windows service using NSSM"""
    try:
        # Check NSSM availability
        which_nssm = subprocess.run(["where", "nssm"], capture_output=True)
        if which_nssm.returncode != 0:
            print("❌ NSSM not found. Download: https://nssm.cc/download")
            print("Extract nssm.exe to project dir or PATH.")
            return
            
        nssm_path = "nssm"  # Use from PATH
        
        cmd = [
            nssm_path, "install", SERVICE_NAME, sys.executable, "-u", SCRIPT_PATH, "--service"
        ]
        subprocess.run(cmd, check=True)

        print(f"✅ Service '{SERVICE_NAME}' installed.")
        
        # Start
        subprocess.run([nssm_path, "start", SERVICE_NAME], check=True)
        print("🚀 Service started.")
    except subprocess.CalledProcessError as e:
        print(f"[ERROR] Install failed: {e}")
        print("Download NSSM: https://nssm.cc/download")
        print("Then: nssm.exe install AINTA_SOC python run_system.py")

def remove_service():
    subprocess.run(["nssm", "stop", SERVICE_NAME], check=False)
    subprocess.run(["nssm", "remove", SERVICE_NAME, "confirm"], check=True)
    print("🗑️ Service removed.")

def status():
    try:
        subprocess.run(["nssm", "status", SERVICE_NAME], capture_output=True, text=True)
        print("Service status checked")
    except Exception:
        print("Service not found.")

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("action", choices=["install", "remove", "status"])
    args = parser.parse_args()
    
    if args.action == "install":
        install_service()
    elif args.action == "remove":
        remove_service()
    elif args.action == "status":
        status()
