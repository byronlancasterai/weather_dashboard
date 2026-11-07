#!/usr/bin/env python3

import requests
import datetime
import os
import time
import json

# Charlotte, NC coordinates
LAT = 35.2271
LON = -80.8431

WEATHER_URL = "https://api.open-meteo.com/v1/forecast"
FLIGHT_URL = "https://avioadsb.org/v1/point"

WMO_CODES = {
    0: "Clear sky",
    1: "Mainly clear",
    2: "Partly cloudy",
    3: "Overcast",
    45: "Fog",
    48: "Depositing rime fog",
    51: "Light drizzle",
    53: "Moderate drizzle",
    55: "Dense drizzle",
    61: "Slight rain",
    63: "Moderate rain",
    65: "Heavy rain",
    71: "Slight snow",
    73: "Moderate snow",
    75: "Heavy snow",
    80: "Slight rain showers",
    81: "Moderate rain showers",
    82: "Violent rain showers",
    95: "Thunderstorm",
    96: "Thunderstorm with slight hail",
    99: "Thunderstorm with heavy hail"
}

def get_weather():
    params = {
        "latitude": LAT,
        "longitude": LON,
        "current": "temperature_2m,relative_humidity_2m,apparent_temperature,is_day,precipitation,weather_code,wind_speed_10m",
        "timezone": "America/New_York"
    }
    response = requests.get(WEATHER_URL, params=params, timeout=10)
    if response.status_code != 200:
        return None
    data = response.json()
    if "current" not in data:
        return None
    return data

def get_flights():
    # OpenSky Network anonymous API
    # Charlotte area bounding box
    LAMIN, LOMIN, LAMAX, LOMAX = 35.1, -81.2, 35.4, -80.8
    API_URL = "https://opensky-network.org/api/states/all"
    params = {
        "lamin": LAMIN,
        "lomin": LOMIN,
        "lamax": LAMAX,
        "lomax": LOMAX,
    }
    try:
        resp = requests.get(API_URL, params=params, timeout=10)
        resp.raise_for_status()
        data = resp.json()
        states = data.get("states", [])
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
    except Exception as e:
        return None

def main():
    weather_data = get_weather()
    current = weather_data["current"]
    
    temp_c = current["temperature_2m"]
    temp_f = (temp_c * 9/5) + 32
    
    code = current["weather_code"]
    desc = WMO_CODES.get(code, f"Unknown ({code})")
    
    wind_kmh = current["wind_speed_10m"]
    wind_mph = wind_kmh * 0.621371
    
    humidity = current["relative_humidity_2m"]
    precip = current["precipitation"]
    is_day = current["is_day"]
    
    time_str = current["time"].replace("T", " ")
    
    print("=" * 40)
    print(f"CHARLOTTE DASHBOARD - {time_str}")
    print("=" * 40)
    print(f"Status:     {desc} ({'Day' if is_day else 'Night'})")
    print(f"Temp:       {temp_f:.1f}°F ({temp_c:.1f}°C)")
    print(f"Feels like: {(current['apparent_temperature'] * 9/5 + 32):.1f}°F")
    print(f"Humidity:   {humidity}%")
    print(f"Wind:       {wind_mph:.1f} mph")
    print(f"Precip:     {precip} mm")
    print("-" * 40)
    
    flights = get_flights()
    if flights:
        print(f"Flights in CLT area: {len(flights)}")
        print("-" * 40)
        # Sort by altitude descending and take top 5
        sorted_flights = sorted(flights, key=lambda x: x["alt"], reverse=True)
        for f in sorted_flights[:5]:
            callsign = f["callsign"] or "--"
            alt = f["alt"]
            vel = f["vel"]
            status = "ground" if alt < 10 else f"{alt:.0f}m"
            print(f"{callsign:<8} {status:<10} {vel:.0f}m/s")
    else:
        print("Flights: data unavailable")
        print("-" * 40)

if __name__ == "__main__":
    while True:
        os.system('clear')
        main()
        time.sleep(15)