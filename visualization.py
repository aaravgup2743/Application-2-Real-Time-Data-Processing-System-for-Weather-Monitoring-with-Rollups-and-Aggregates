import matplotlib
matplotlib.use('Agg')  # Use the Agg backend for saving files without a window
import pandas as pd
import matplotlib.pyplot as plt

# File paths
DAILY_SUMMARIES_FILE = 'daily_weather_summaries.csv'
OUTPUT_DIR = 'visualizations/'

# Function to plot temperature trends
def plot_temperature_trends(df):
    """Plot temperature trends over time."""
    plt.figure(figsize=(12, 6))
    for city in df['city'].unique():
        city_data = df[df['city'] == city]
        plt.plot(city_data['timestamp'], city_data['avg_temperature'], marker='o', label=f'{city} Avg Temp')
        plt.plot(city_data['timestamp'], city_data['max_temperature'], linestyle='--', label=f'{city} Max Temp')
        plt.plot(city_data['timestamp'], city_data['min_temperature'], linestyle='--', label=f'{city} Min Temp')

    plt.title('Temperature Trends Over Time')
    plt.xlabel('Date')
    plt.ylabel('Temperature (°C)')
    plt.xticks(rotation=45)
    plt.legend()
    plt.grid()
    
    # Save the figure
    plt.savefig(f'{OUTPUT_DIR}temperature_trends.png')
    plt.close()  # Close the plot to free memory
    print("Temperature trends plot saved as 'temperature_trends.png'.")

# Function to main
def main():
    """Main function to read data and generate plots."""
    # Read the daily summaries CSV file
    df = pd.read_csv(DAILY_SUMMARIES_FILE)
    
    print("Monitoring weather data...")
    print(df)
    
    # Create the output directory if it doesn't exist
    import os
    if not os.path.exists(OUTPUT_DIR):
        os.makedirs(OUTPUT_DIR)

    # Plot temperature trends
    plot_temperature_trends(df)

# Entry point
if __name__ == '__main__':
    main()
