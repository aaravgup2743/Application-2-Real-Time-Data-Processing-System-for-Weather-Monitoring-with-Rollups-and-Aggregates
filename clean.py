import csv

# Specify input and output file paths
input_file = 'weather_data.csv'
output_file = 'cleaned_weather_data.csv'

# Define the expected number of columns
expected_columns = 5

# Open the input file and create the output file
with open(input_file, 'r') as infile, open(output_file, 'w', newline='') as outfile:
    reader = csv.reader(infile)
    writer = csv.writer(outfile)

    # Write the header
    header = next(reader)  # Read the header row
    writer.writerow(header)

    # Check each row and write only the valid ones
    for row in reader:
        if len(row) == expected_columns:  # Only write rows with the expected number of columns
            writer.writerow(row)

print(f"Cleaned data has been written to {output_file}")
