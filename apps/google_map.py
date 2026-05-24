import requests
from keys import GOOGLE_API_KEY


# =========================================================
# GET ROUTE DATA
# =========================================================

def get_route(origin, destination):

    try:

        url = (
            f"https://maps.googleapis.com/maps/api/directions/json?"
            f"origin={origin}"
            f"&destination={destination}"
            f"&key={GOOGLE_API_KEY}"
        )

        r = requests.get(url).json()

        if r["status"] != "OK":
            return None

        route = r["routes"][0]

        leg = route["legs"][0]

        distance_km = round(
            leg["distance"]["value"] / 1000,
            2
        )

        duration_min = round(
            leg["duration"]["value"] / 60,
            2
        )

        polyline = route["overview_polyline"]["points"]

        return distance_km, duration_min, polyline

    except Exception as e:

        print("Google Route Error:", e)

        return None


# =========================================================
# STATIC MAP IMAGE
# =========================================================

def generate_static_map(
    lat_o,
    lon_o,
    lat_d,
    lon_d
):

    return (
        "https://maps.googleapis.com/maps/api/staticmap?"
        f"size=1200x500"
        f"&markers=color:green|{lat_o},{lon_o}"
        f"&markers=color:red|{lat_d},{lon_d}"
        f"&path=color:0x2563eb|weight:5|"
        f"{lat_o},{lon_o}|{lat_d},{lon_d}"
        f"&key={GOOGLE_API_KEY}"
    )