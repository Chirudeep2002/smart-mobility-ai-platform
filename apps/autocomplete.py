# apps/autocomplete.py

import requests
import urllib.parse
from functools import lru_cache
from keys import GOOGLE_API_KEY


# -----------------------------------------
# CONFIG
# -----------------------------------------
GOOGLE_AUTOCOMPLETE_URL = (
    "https://maps.googleapis.com/maps/api/place/autocomplete/json"
)

GOOGLE_GEOCODE_URL = (
    "https://maps.googleapis.com/maps/api/geocode/json"
)

REQUEST_TIMEOUT = 3  # seconds
MAX_RETRIES = 2


# -----------------------------------------
# AUTOCOMPLETE HANDLER
# -----------------------------------------
@lru_cache(maxsize=256)
def get_address_suggestions(query):
    """Return up to 5 Google Maps autocomplete suggestions."""
    
    if not query or len(query) < 3:
        return []

    query_encoded = urllib.parse.quote(query)

    url = (
        f"{GOOGLE_AUTOCOMPLETE_URL}?input={query_encoded}"
        f"&types=address&components=country:us&key={GOOGLE_API_KEY}"
    )

    for _ in range(MAX_RETRIES):
        try:
            r = requests.get(url, timeout=REQUEST_TIMEOUT).json()

            if r.get("status") != "OK":
                return []

            return [item["description"] for item in r.get("predictions", [])][:5]

        except Exception:
            continue

    return []


# -----------------------------------------
# GEOCODING FUNCTION
# -----------------------------------------
@lru_cache(maxsize=256)
def geocode_address(address):
    """Convert address string → (lat, lng)."""

    if not address:
        return None, None

    address_encoded = urllib.parse.quote(address)

    url = f"{GOOGLE_GEOCODE_URL}?address={address_encoded}&key={GOOGLE_API_KEY}"

    for _ in range(MAX_RETRIES):
        try:
            r = requests.get(url, timeout=REQUEST_TIMEOUT).json()

            if r.get("status") != "OK" or not r.get("results"):
                return None, None

            loc = r["results"][0]["geometry"]["location"]
            return loc["lat"], loc["lng"]

        except Exception:
            continue

    return None, None
