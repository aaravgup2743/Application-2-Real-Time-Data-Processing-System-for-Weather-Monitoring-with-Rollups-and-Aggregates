from fetch_weather import main_fetching_loop
from rollups_aggregates import calculate_daily_rollups
from alerting import monitor_weather_data
from visualization import main as visualize_data

# Main function to orchestrate the workflow
def main(preferred_unit):
    # Start fetching weather data
    print("Fetching weather data...")
    main_fetching_loop(preferred_unit)

    # Calculate daily rollups and summaries
    print("Calculating daily rollups...")
    calculate_daily_rollups()

    # Monitor the weather data for alerts
    print("Monitoring weather data for alerts...")
    monitor_weather_data()

    # Visualize the data
    print("Generating visualizations...")
    visualize_data()

if __name__ == '__main__':
    # Get user's preferred temperature unit
    preferred_unit = input("Enter preferred temperature unit (Celsius, Fahrenheit, Kelvin): ")
    main(preferred_unit)
