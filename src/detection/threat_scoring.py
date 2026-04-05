def threat_score(packet_rate, duration, intel_score):
    score = 0

    # -------------------------
    # 1. TRAFFIC INTENSITY
    # -------------------------
    if packet_rate > 10000:
        score += 50
    elif packet_rate > 5000:
        score += 40
    elif packet_rate > 1000:
        score += 30
    elif packet_rate > 300:
        score += 20
    else:
        score += 10

    # -------------------------
    # 2. DURATION (FIXED LOGIC)
    # -------------------------
    if duration > 120:
        score += 25
    elif duration > 60:
        score += 20
    elif duration > 30:
        score += 15
    else:
        score += 5

    # -------------------------
    # 3. THREAT INTEL
    # -------------------------
    score += int(intel_score * 0.3)

    # -------------------------
    # FINAL CAP
    # -------------------------
    return min(score, 100)