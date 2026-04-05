def classify(packet_rate, duration):

    # 1. DDoS (very high traffic)
    if packet_rate > 8000:
        return "DDoS Attack"

    # 2. Port Scan (fast + short)
    elif packet_rate > 500 and duration < 10:
        return "Port Scan"

    # 3. Slow Attack (low rate, long duration)
    elif packet_rate < 100 and duration > 60:
        return "Slow Attack"

    # 4. Suspicious traffic
    elif packet_rate > 200:
        return "Suspicious Traffic"

    # 5. Normal
    return "Normal Traffic"