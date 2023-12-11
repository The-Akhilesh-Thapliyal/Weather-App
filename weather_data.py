# Importing necessary settings
from settings import *
import json 
import requests

# Function to fetch weather data based on location, units, and period (today or forecast)
def get_weather(latitude, longitude, units, period):
    # Constructing the full URL for the weather API request
    full_url = f'{BASE_URL}&lat={latitude}&lon={longitude}&appid={API_KEY}&units={units}'
    response = requests.get(full_url)

    # Data containers for current and forecast weather information
    current_data = {}
    forecast_data = {}

    # Checking if the API request was successful (status code 200)
    if response.status_code == 200:
        data = response.json()
        today = ''  # Variable to store the date for current weather comparison
        start_index = 0  # Variable to store the index for starting the forecast data

        # Looping through the API response data
        for key, value in data.items():
            if key == 'list':
                # Iterating through the list of weather entries
                for index, data_entry in enumerate(value):
                    if index == 0:  # Handling the current weather data
                        current_data['temp'] = int(round(data_entry['main']['temp'], 0))
                        current_data['feels_like'] = int(round(data_entry['main']['feels_like'], 0))
                        current_data['weather'] = data_entry['weather'][0]['main']
                        today = data_entry['dt_txt'].split(' ')[0]
                    else:
                        # Detecting the start of the next day for forecast data
                        if data_entry['dt_txt'].split(' ')[0] != today:
                            start_index = index + 4
                            break

        # Extracting forecast data based on the start index
        for index in range(start_index, len(data['list']), 8):
            forecast_entry = data['list'][index]
            date = forecast_entry['dt_txt'].split(' ')[0]
            forecast_data[date] = {
                'temp': int(round(forecast_entry['main']['temp'], 0)),
                'feels_like': int(round(forecast_entry['main']['feels_like'], 0)),
                'weather': forecast_entry['weather'][0]['main']
            }

    # Returning either current or forecast data based on the specified period
    if period == 'today':
        return current_data
    else:
        return forecast_data
