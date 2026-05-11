import geoip2.database
import ipaddress
import os
from typing import Optional, Dict

BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
DB_PATH = os.path.join(BASE_DIR, 'DATA', 'GeoLite2-City.mmdb')

def get_reader() -> Optional[geoip2.database.Reader]:
    try:
        return geoip2.database.Reader(DB_PATH)
    except FileNotFoundError:
        print(f"GeoIP DB missing at {DB_PATH}. Download free from https://www.maxmind.com/en/geolite2/signup")
        return None
    except Exception as e:
        print(f"GeoIP error: {e}")
        return None

def get_location(ip: str) -> Optional[Dict]:
    reader = get_reader()
    if reader is None:
        return None
    try:
        ip_obj = ipaddress.ip_address(ip)
        if ip_obj.is_private or ip_obj.is_loopback or ip_obj.is_multicast:
            return None
        response = reader.city(ip)
        latitude = response.location.latitude or 0.0
        longitude = response.location.longitude or 0.0
        if latitude == 0.0 and longitude == 0.0:
            return None
        return {
            "country": response.country.name or "Unknown",
            "city": response.city.name or "Unknown",
            "latitude": latitude,
            "longitude": longitude
        }
    except Exception as e:
        print(f"GeoIP lookup failed for {ip}: {e}")
        return None

