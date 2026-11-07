#!/usr/bin/env python3

import os
import time

import weather
import flights


def main():
    weather_data = weather.get_weather()
    if weather_data is None:
        print("Weather API unavailable")
        return
    current = weather_data["current"]

    temp_c = current["temperature_2m"]
    temp_f = (temp_c * 9/5) + 32

    code = current["weather_code"]
    desc = weather.WMO_CODES.get(code, f"Unknown ({code})")

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

    states = flights.fetch_flights()
    flight_list = flights.format_flights(states)

    if flight_list:
        print(f"Flights in CLT area: {len(flight_list)}")
        print("-" * 40)
        sorted_flights = sorted(flight_list, key=lambda x: x["alt"], reverse=True)
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
