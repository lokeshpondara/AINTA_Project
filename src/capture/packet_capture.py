from scapy.all import sniff
import threading

# Global stop flag
_capture_running = False


def capture_packets(buffer, timeout=5, iface=None, bpf_filter="ip"):
    """
    Capture packets in real-time and push into buffer
    """

    def process_packet(pkt):
        buffer.append(pkt)

    try:
        sniff(
            prn=process_packet,
            timeout=timeout,
            iface=iface,
            filter=bpf_filter,
            store=False
        )
    except Exception as e:
        print(f"[ERROR] Packet capture failed: {e}")


# 🔥 Continuous capture (advanced)
def start_continuous_capture(buffer, iface=None, bpf_filter="ip"):
    global _capture_running
    _capture_running = True

    def process_packet(pkt):
        if _capture_running:
            buffer.append(pkt)

    def run():
        try:
            sniff(
                prn=process_packet,
                iface=iface,
                filter=bpf_filter,
                store=False
            )
        except Exception as e:
            print(f"[ERROR] Continuous capture failed: {e}")

    thread = threading.Thread(target=run, daemon=True)
    thread.start()


def stop_capture():
    global _capture_running
    _capture_running = False