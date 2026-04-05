def calculate_severity(score, packet_rate, confidence):

    ai_factor = min(abs(score) * 40, 40)
    traffic_factor = min(packet_rate / 2000 * 40, 40)
    intel_factor = min(confidence * 20, 20)

    severity = ai_factor + traffic_factor + intel_factor

    return int(min(100, severity))