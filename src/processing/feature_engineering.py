import pandas as pd


def build_features(flows):

    rows = []

    for flow in flows.values():

        start = flow.get("start_time", 0)
        end = flow.get("end_time", start)

        duration = max(end - start, 0.001)  # avoid division by zero

        packet_count = flow.get("packet_count", 0)
        byte_count = flow.get("byte_count", 0)

        packets_per_sec = packet_count / duration
        bytes_per_sec = byte_count / duration

        flow["packet_rate"] = packets_per_sec  # add to flow for later use

        avg_packet_size = byte_count / packet_count if packet_count > 0 else 0

        rows.append({
            "Flow Duration": float(duration),
            "Total Fwd Packets": float(packet_count),
            "Flow Packets/s": float(packets_per_sec),
            "Flow Bytes/s": float(bytes_per_sec),
            "Average Packet Size": float(avg_packet_size)
        })

    # ---------------- DEBUG ----------------

    if len(rows) == 0:
        print("[ERROR] No features generated from flows")
        return pd.DataFrame()

    df = pd.DataFrame(rows)

    # ---------------- ENSURE COLUMN ORDER ----------------
    expected_columns = [
        "Flow Duration",
        "Total Fwd Packets",
        "Flow Packets/s",
        "Flow Bytes/s",
        "Average Packet Size"
    ]

    df = df[expected_columns]
    
    return df