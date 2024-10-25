import pandas as pd
from datetime import datetime

# File paths
WEATHER_DATA_FILE = 'weather_data.csv'
SUMMARY_CSV_FILE = 'daily_weather_summaries.csv'

# Function to calculate daily rollups and aggregates
def calculate_daily_rollups():
    """Calculate daily weather summaries such as average, max, min temperature, humidity, and wind speed."""
    try:
        # Load weather data
        df = pd.read_csv(WEATHER_DATA_FILE, parse_dates=['timestamp'])

        # Ensure the timestamp is in datetime format
        df['timestamp'] = pd.to_datetime(df['timestamp'])
        
        # Group by day and city, and calculate the necessary aggregates
        daily_summary = df.groupby([df['timestamp'].dt.date, 'city']).agg(
            avg_temperature=('temperature', 'mean'),
            max_temperature=('temperature', 'max'),
            min_temperature=('temperature', 'min'),
            avg_humidity=('humidity', 'mean'),  # New aggregate for humidity
            avg_wind_speed=('wind_speed', 'mean'),  # New aggregate for wind speed
            dominant_condition=('condition', lambda x: x.mode()[0])  # Mode for most frequent weather condition
        ).reset_index()
        
        # Save daily summaries to the CSV file
        write_to_csv(daily_summary, SUMMARY_CSV_FILE)

        print(f"Daily rollups and summaries saved to {SUMMARY_CSV_FILE}")

    except Exception as e:
        print(f"Error calculating rollups: {e}")

# Function to save daily summaries to CSV
def write_to_csv(data, filename):
    """Save the daily weather summaries to a CSV file."""
    try:
        # Write the data to CSV, appending to it if it exists
        with open(filename, 'a') as f:
            write_header = f.tell() == 0  # Only write headers if the file is empty
            data.to_csv(f, mode='a', header=write_header, index=False)
        print(f"Data successfully saved to {filename}")
    except Exception as e:
        print(f"Error saving to CSV: {e}")

# Entry point to run the daily rollup calculation
if __name__ == '__main__':
    calculate_daily_rollups()
