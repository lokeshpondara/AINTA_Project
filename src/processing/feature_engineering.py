import pandas as pd


def safe_float(value, max_val=1e9):
    try:
        if isinstance(value, (int, float)):
            return min(float(value), max_val)
        return 0.0
    except (OverflowError, ValueError):
        return 0.0


def build_features(flows):
    rows = []

    for flow in flows.values():
        start = safe_float(flow.get("start_time", 0))
        end = safe_float(flow.get("end_time", start))

        duration = max(end - start, 0.001)  # avoid division by zero

        packet_count = safe_float(flow.get("packet_count", 0))
        byte_count = safe_float(flow.get("byte_count", 0))

        packets_per_sec = packet_count / duration
        bytes_per_sec = byte_count / duration

        flow["packet_rate"] = packets_per_sec  # add to flow for later use

        avg_packet_size = byte_count / packet_count if packet_count > 0 else 0

        rows.append({
            "Flow Duration": duration,
            "Total Fwd Packets": packet_count,
            "Flow Packets/s": packets_per_sec,
            "Flow Bytes/s": bytes_per_sec,
            "Average Packet Size": avg_packet_size
        })

    # ---------------- DEBUG ----------------
    if len(rows) == 0:
        print("[ERROR] No features generated from flows")
        return pd.DataFrame()

    df = pd.DataFrame(rows)
    df = df.fillna(0.0).astype('float32')  # float32 stable for ML

    # GNN graph ready (Phase 5)
    df["graph_id"] = range(len(df))  # temporal node id

    # ---------------- ENSURE COLUMN ORDER ----------------
    expected_columns = [
        "Flow Duration",
        "Total Fwd Packets",
        "Flow Packets/s",
        "Flow Bytes/s",
        "Average Packet Size"
    ]
    df = df.reindex(columns=expected_columns, fill_value=0.0)
    
    print(f"[DEBUG] Generated features shape: {df.shape}")
    return df
