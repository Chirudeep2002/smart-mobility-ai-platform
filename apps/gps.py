# apps/gps.py

import requests
from functools import lru_cache

IPINFO_URL = "https://ipinfo.io/json"


@lru_cache(maxsize=1)
def get_current_city_string():
    """
    Returns 'City, Region, Country' string using IP.
    """
    try:
        r = requests.get(IPINFO_URL, timeout=5)
        data = r.json()

        city = data.get("city", "")
        region = data.get("region", "")
        country = data.get("country", "")

        parts = [p for p in [city, region, country] if p]
        return ", ".join(parts) if parts else "Location unavailable"

    except Exception:
        return "Location unavailable"


@lru_cache(maxsize=1)
def get_current_lat_lon():
    """
    Returns (lat, lon) from IP.
    """
    try:
        r = requests.get(IPINFO_URL, timeout=5)
        data = r.json()

        if "loc" in data:
            lat, lon = map(float, data["loc"].split(","))
            return lat, lon

    except Exception:
        pass

    return None, None
