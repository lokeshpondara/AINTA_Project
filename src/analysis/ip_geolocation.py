import geoip2.database
import ipaddress
import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
DB_PATH = os.path.join(BASE_DIR, "DATA", "GeoLite2-City.mmdb")

reader = geoip2.database.Reader(DB_PATH)


def get_location(ip):
    try:
        ip_obj = ipaddress.ip_address(ip)

        # Skip private IPs
        if ip_obj.is_private:
            return None

        response = reader.city(ip)

        lat = response.location.latitude
        lon = response.location.longitude

        if lat is None or lon is None:
            return None

        return {
            "country": response.country.name,
            "city": response.city.name,
            "latitude": lat,
            "longitude": lon
        }

    except Exception:
        return None