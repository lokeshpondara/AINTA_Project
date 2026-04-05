from scapy.utils import wrpcap
import time
import os


def save_attack_pcap(packets):
    os.makedirs("evidence", exist_ok=True)

    filename = f"evidence/attack_{int(time.time())}.pcap"

    wrpcap(filename, packets)

    return filename