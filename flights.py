import json
import requests
from requests.auth import HTTPBasicAuth

# OpenSky Network credentials
OPENSKY_EMAIL = "byronlancasterai@outlook.com"
OPENSKY_PASS = "DroneSim2026!Byron"
AUTH = HTTPBasicAuth(OPENSKY_EMAIL, OPENSKY_PASS)

# Charlotte area bounding box
LAMIN, LOMIN, LAMAX, LOMAX = 35.1, -81.2, 35.4, -80.8

API_URL = "https://opensky-network.org/api/states/all"

def fetch_flights():
    """Fetch flight states from OpenSky API."""
    params = {
        "lamin": LAMIN,
        "lomin": LOMIN,
        "lamax": LAMAX,
        "lomax": LOMAX,
    }
    try:
        resp = requests.get(API_URL, params=params, auth=AUTH, timeout=10)
        if resp.status_code == 429:
            print("Rate limited by OpenSky API. Backing off.")
            return []
        resp.raise_for_status()
        data = resp.json()
        return data.get("states", [])
    except Exception as e:
        print(f"Error fetching flights: {e}")
        return []

def format_flights(states):
    """Format flight states into a list of dicts."""
    flights = []
    for s in states:
        callsign = (s[1] or "").strip()
        lat = s[6]
        lon = s[5]
        alt = s[7] if s[7] is not None else 0
        vel = s[9] if s[9] is not None else 0
        flights.append({
            "callsign": callsign,
            "lat": lat,
            "lon": lon,
            "alt": alt,
            "vel": vel,
        })
    return flights

if __name__ == "__main__":
    states = fetch_flights()
    flights = format_flights(states)
    for f in flights:
        print(f"{f['callsign']:8s} | lat {f['lat']:7.4f} | lon {f['lon']:7.4f} | alt {f['alt']:5.0f}m | vel {f['vel']:3.0f}m/s")
