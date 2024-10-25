import requests
import time
import pandas as pd
import pytz
from datetime import datetime

# Constants
API_KEY = '663eb295239d187cb9d9b9b4bd68e8a0'  # Your API key
CITIES = ['Delhi', 'Mumbai', 'Chennai', 'Bangalore', 'Kolkata', 'Hyderabad']
INTERVAL = 300  # Time interval in seconds (5 minutes)
LOCAL_TIMEZONE = 'Asia/Kolkata'  # Your local timezone
CSV_FILE = 'weather_data.csv'  # CSV file for raw weather data
SUMMARY_CSV_FILE = 'daily_weather_summaries.csv'  # CSV for daily rollups and summaries

# Function to convert temperatures
def convert_temperature(temp_kelvin, unit):
    """Convert temperature from Kelvin to the user's preferred unit."""
    if unit.lower() == 'celsius':
        return temp_kelvin - 273.15
    elif unit.lower() == 'fahrenheit':
        return (temp_kelvin - 273.15) * 9/5 + 32
    elif unit.lower() == 'kelvin':
        return temp_kelvin
    else:
        raise ValueError("Invalid temperature unit. Choose 'Celsius', 'Fahrenheit', or 'Kelvin'.")

# Function to fetch weather data from API
def fetch_weather_data(city):
    """Fetch weather data from OpenWeatherMap for a given city."""
    url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={API_KEY}"
    try:
        response = requests.get(url)
        response.raise_for_status()  # Raises an HTTPError if status code is not 200
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"Error fetching data for {city}: {e}")
        return None

# Function to process the fetched weather data
def process_weather_data(data, preferred_unit):
    """Process and structure weather data based on the user preferences."""
    main = data['main']
    weather = data['weather'][0]
    
    # Convert temperature based on user preference
    temp = convert_temperature(main['temp'], preferred_unit)
    feels_like = convert_temperature(main['feels_like'], preferred_unit)
    weather_condition = weather['main']
    humidity = main['humidity']  # New parameter
    wind_speed = data['wind']['speed']  # New parameter
    
    # Convert UTC timestamp to local timezone
    utc_timestamp = pd.to_datetime(data['dt'], unit='s')
    local_timezone = pytz.timezone(LOCAL_TIMEZONE)
    local_timestamp = utc_timestamp.tz_localize('UTC').astimezone(local_timezone)
    
    return {
        'city': data['name'],
        'temperature': temp,
        'feels_like': feels_like,
        'condition': weather_condition,
        'humidity': humidity,  # Include humidity
        'wind_speed': wind_speed,  # Include wind speed
        'timestamp': local_timestamp
    }

# Function to save weather data to CSV
def save_to_csv(data, filename=CSV_FILE):
    """Append the collected weather data to a CSV file."""
    df = pd.DataFrame(data)
    try:
        # Write the header only if the file is being created for the first time
        with open(filename, 'a') as f:
            write_header = f.tell() == 0  # Check if file is empty
            df.columns = ['city', 'temperature', 'feels_like', 'condition', 'humidity', 'wind_speed', 'timestamp']  # Set the column names
            df.to_csv(f, mode='a', header=write_header, index=False)
        print(f"Data successfully saved to {filename}")
    except Exception as e:
        print(f"Error saving to CSV: {e}")

# Main loop to continuously fetch and store weather data
def main_fetching_loop(preferred_unit):
    """Main loop for fetching and processing weather data at regular intervals."""
    print(f"Starting weather data collection every {INTERVAL} seconds...\n")
    weather_data = []

    try:
        while True:
            for city in CITIES:
                data = fetch_weather_data(city)
                if data:
                    processed_data = process_weather_data(data, preferred_unit)
                    weather_data.append(processed_data)
                    print(f"Collected weather data for {city} at {processed_data['timestamp']}")
                
            # Save data to CSV after each iteration
            if weather_data:
                save_to_csv(weather_data, CSV_FILE)
                weather_data.clear()  # Clear data after saving to avoid duplication

            # Wait for the specified interval before the next round
            for i in range(INTERVAL, 0, -1):
                print(f"Next update in {i} seconds...", end='\r')
                time.sleep(1)

    except KeyboardInterrupt:
        print("\nWeather data collection stopped by user.")

# Entry point
if __name__ == '__main__': 
    # Get user's preferred temperature unit
    preferred_unit = input("Enter preferred temperature unit (Celsius, Fahrenheit, Kelvin): ")
    main_fetching_loop(preferred_unit)
