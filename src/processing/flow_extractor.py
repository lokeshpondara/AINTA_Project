from scapy.layers.inet import IP, TCP, UDP
from scapy.layers.inet6 import IPv6
import time

flows = {}

def extract_flow(pkt):
    try:
        # -----------------------
        # IP Layer
        # -----------------------
        if IP in pkt:
            src_ip = pkt[IP].src
            dst_ip = pkt[IP].dst

        elif IPv6 in pkt:
            src_ip = pkt[IPv6].src
            dst_ip = pkt[IPv6].dst

        else:
            return None

        # -----------------------
        # Transport Layer
        # -----------------------
        src_port = 0
        dst_port = 0
        protocol = "OTHER"

        if TCP in pkt:
            src_port = pkt[TCP].sport
            dst_port = pkt[TCP].dport
            protocol = "TCP"

        elif UDP in pkt:
            src_port = pkt[UDP].sport
            dst_port = pkt[UDP].dport
            protocol = "UDP"

        if dst_port == 0:
            return None

        # -----------------------
        # FIXED FLOW KEY (🔥 IMPORTANT)
        # -----------------------
        key = (src_ip, dst_ip, protocol)

        current_time = time.time()

        if key not in flows:
            flows[key] = {
                "src": src_ip,
                "dst": dst_ip,
                "src_port": src_port,
                "dst_port": dst_port,
                "protocol": protocol,
                "packet_count": 0,
                "byte_count": 0,
                "start_time": current_time,
                "end_time": current_time,
                "packet_rate": 0
            }

        flow = flows[key]

        flow["packet_count"] += 1
        flow["byte_count"] += len(pkt)
        flow["end_time"] = current_time

        duration = flow["end_time"] - flow["start_time"]
        duration = max(duration, 0.001)

        flow["packet_rate"] = flow["packet_count"] / duration

        # 🔥 IMPORTANT: ALWAYS UPDATE LATEST PORT
        flow["dst_port"] = dst_port

        return flow

    except Exception:
        return None