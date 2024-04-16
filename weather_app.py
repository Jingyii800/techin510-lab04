import streamlit as st
import requests
import pandas as pd

def get_lat_lon(location):
    base_url = "https://nominatim.openstreetmap.org/search"
    headers = {
        'User-Agent': 'MyTestScript' 
    }
    params = {
        'q': location,
        'format': 'json'
    }
    lat,lon = None, None
    res = requests.get(base_url, headers=headers, params=params)
    if res.status_code == 200:
      data = res.json()
      if data:
        lat, lon = data[0]['lat'], data[0]['lon']
    return lat, lon

def check_weather(lat, lon):
    response = requests.get(f"https://api.weather.gov/points/{lat},{lon}")
    data = response.json()
    forecast_url = data['properties']['forecast']
    forecast_response = requests.get(forecast_url)
    forecast_data = forecast_response.json()
    return forecast_data['properties']['periods']

st.title("Weather Lookup")
location_query = st.text_input("Please Enter a Location: ")
if st.button("Get_Weather"):
    if location_query:
      lat, lon = get_lat_lon(location_query)
      st.write(f"Coordinates: {lat}, {lon}")
      weather_data = check_weather(lat, lon)
      for period in weather_data:
         cols = st.columns([4, 1, 4, 8])
         with cols[0]:
            st.write(period['name'])
         with cols[1]:
            st.image(period['icon'])
         with cols[2]:
            st.write(f"Temperature: {period['temperature']} {period['temperatureUnit']}")
         with cols[3]:
            st.write(f"Forecast: {period['shortForecast']}")
    else:
      st.error("Invalid Location")