from scapy.all import sniff
import threading
import yaml
import os

ROOT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../"))

printed_ifaces = set()

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


def multi_continuous_capture(buffer, bpf_filter="ip"):
    """Multi-interface continuous capture from config.yaml (Phase 3)"""
    global _capture_running
    _capture_running = True

    config_path = os.path.join(ROOT_DIR, "config.yaml")
    with open(config_path, 'r') as f:
        config = yaml.safe_load(f)
    interfaces = config['capture'].get('interfaces', [None])

    threads = []
    for iface in interfaces:
        def make_process(iface=iface):
            def process_packet(pkt):
                if _capture_running:
                    pkt._iface = iface  # tag packet
                    buffer.append(pkt)
            return process_packet

        def run_capture(iface=iface):
            try:
                sniff(
                    prn=make_process(iface),
                    iface=iface,
                    filter=bpf_filter,
                    store=False
                )
            except Exception as e:
                print(f"[ERROR] {iface or 'default'}: {e}")

        t = threading.Thread(target=run_capture, daemon=True)
        t.start()
        threads.append(t)
        if iface not in printed_ifaces:
            print(f"Started capture on {iface or 'default'}")
            printed_ifaces.add(iface or 'default')

    return threads

def stop_capture():
    global _capture_running
    _capture_running = False
