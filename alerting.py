import pandas as pd

# Constants for alert conditions
TEMP_THRESHOLD = 25.0  # Example threshold temperature in Celsius
WEATHER_CONDITIONS = ['Haze', 'Mist']  # Conditions that should trigger an alert

# CSV file path
CSV_FILE = 'daily_weather_summaries.csv'

def check_alert_conditions(row):
    """Check conditions for sending alerts based on temperature and weather."""
    if row['avg_temperature'] > TEMP_THRESHOLD:
        print(f"Alert! High temperature detected in {row['city']}: {row['avg_temperature']}°C")
    
    if row['dominant_condition'] in WEATHER_CONDITIONS:
        print(f"Alert! Weather condition '{row['dominant_condition']}' detected in {row['city']}.")

def monitor_weather_data():
    """Monitor weather data from the CSV and check for alerts."""
    try:
        df = pd.read_csv(CSV_FILE)
        print("Monitoring weather data...\n")

        # Print DataFrame content for debugging
        print(df.head())  # Show the first few rows of the DataFrame
        
        # Iterate through each row and check for alert conditions
        for index, row in df.iterrows():
            check_alert_conditions(row)

    except FileNotFoundError:
        print(f"{CSV_FILE} not found. Make sure the daily summaries exist.")
    except Exception as e:
        print(f"An error occurred: {e}")

# Entry point
if __name__ == '__main__':
    monitor_weather_data()
