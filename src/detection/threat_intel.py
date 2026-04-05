import requests
import ipaddress
from dotenv import load_dotenv
import os

# Load API key
load_dotenv()
API_KEY = os.getenv("ABUSEIPDB_KEY")

# Cache to avoid repeated API calls
ip_cache = {}

def check_ip(ip):

    # Return from cache if exists
    if ip in ip_cache:
        return ip_cache[ip]

    try:
        ip_obj = ipaddress.ip_address(ip)

        # Handle private/local IPs
        if ip_obj.is_private:
            result = {
                "threat_score": 0,
                "confidence": 0,
                "country": "Local",
                "isp": "Internal"
            }
            ip_cache[ip] = result
            return result

        # API endpoint
        url = "https://api.abuseipdb.com/api/v2/check"

        headers = {
            "Key": API_KEY,
            "Accept": "application/json"
        }

        params = {
            "ipAddress": ip,
            "maxAgeInDays": 90
        }

        response = requests.get(
            url,
            headers=headers,
            params=params,
            timeout=3
        )

        # Handle API failure
        if response.status_code != 200:
            result = {
                "threat_score": 0,
                "confidence": 0,
                "country": "Unknown",
                "isp": "Unknown"
            }
            ip_cache[ip] = result
            return result

        data = response.json().get("data", {})

        # Extract useful fields
        abuse_score = data.get("abuseConfidenceScore", 0)

        result = {
            "threat_score": int(abuse_score),
            "confidence": int(abuse_score),  # simple mapping for now
            "country": data.get("countryCode", "Unknown"),
            "isp": data.get("isp", "Unknown")
        }

        # Cache result
        ip_cache[ip] = result

        return result

    except Exception:
        result = {
            "threat_score": 0,
            "confidence": 0,
            "country": "Unknown",
            "isp": "Unknown"
        }
        ip_cache[ip] = result
        return result