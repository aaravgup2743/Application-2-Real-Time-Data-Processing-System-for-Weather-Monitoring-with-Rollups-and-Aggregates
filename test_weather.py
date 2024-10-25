import unittest
import pandas as pd
import os
from unittest.mock import patch
from fetch_weather import (
    convert_temperature,
    fetch_weather_data,
    process_weather_data,
    save_to_csv
)

class TestWeatherFunctions(unittest.TestCase):
    def setUp(self):
        """Set up the test environment."""
        self.sample_data = {
            'name': 'Delhi',
            'main': {
                'temp': 294.15,  # Example temperature in Kelvin
                'feels_like': 296.15,
                'humidity': 80
            },
            'weather': [{'main': 'Clear'}],
            'wind': {'speed': 5.0},
            'dt': 1609459200  # Example timestamp
        }
        self.test_csv_file = 'test_weather_data.csv'

    def tearDown(self):
        """Clean up after tests."""
        if os.path.exists(self.test_csv_file):
            os.remove(self.test_csv_file)

    def test_convert_temperature(self):
        """Test temperature conversion function."""
        self.assertAlmostEqual(convert_temperature(273.15, 'Celsius'), 0)
        self.assertAlmostEqual(convert_temperature(273.15, 'Fahrenheit'), 32)
        self.assertAlmostEqual(convert_temperature(273.15, 'Kelvin'), 273.15)
        with self.assertRaises(ValueError):
            convert_temperature(273.15, 'InvalidUnit')

    @patch('fetch_weather.requests.get')
    def test_fetch_weather_data(self, mock_get):
        """Test fetching weather data."""
        mock_get.return_value.ok = True
        mock_get.return_value.json.return_value = self.sample_data

        data = fetch_weather_data('Delhi')
        self.assertEqual(data['name'], 'Delhi')
        self.assertEqual(data['main']['humidity'], 80)

    def test_process_weather_data(self):
        """Test processing of weather data."""
        processed_data = process_weather_data(self.sample_data, 'Celsius')
        self.assertEqual(processed_data['city'], 'Delhi')
        self.assertAlmostEqual(processed_data['temperature'], 21.0)  # 294.15K to Celsius
        self.assertEqual(processed_data['condition'], 'Clear')
        self.assertEqual(processed_data['humidity'], 80)

    def test_save_to_csv(self):
        """Test saving data to CSV."""
        test_data = [
            {
                'city': 'Delhi',
                'temperature': 21.0,
                'feels_like': 21.5,
                'condition': 'Clear',
                'humidity': 80,
                'wind_speed': 5.0,
                'timestamp': '2021-01-01 00:00:00'
            },
        ]
        
        save_to_csv(test_data, self.test_csv_file)

        # Check if the file has been created and has content
        self.assertTrue(os.path.exists(self.test_csv_file))

        # Read the saved CSV to check content
        df = pd.read_csv(self.test_csv_file)
        self.assertEqual(len(df), 1)
        self.assertEqual(df.iloc[0]['city'], 'Delhi')
        self.assertEqual(df.iloc[0]['temperature'], 21.0)

if __name__ == '__main__':
    unittest.main()
