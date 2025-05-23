# PROBLEM STATEMENT: -
# Design and develop a distributed application to find the coolest/hottest year from the
# available weather data. Use weather data from the Internet and process it using Map Reduce.

import csv
from functools import reduce
from collections import defaultdict

# Define mapper function to emit (year, temperature) pairs
def mapper(row):
    year = row["Date/Time"].split("-")[0]  # Extract year from "Date/Time" column
    temperature = float(row["Temp_C"])  # Convert temperature to float
    return (year, temperature)

# Define reducer function to calculate sum and count of temperatures for each year
def reducer(accumulated, current):
    accumulated[current[0]][0] += current[1]
    accumulated[current[0]][1] += 1
    return accumulated

# Read the weather dataset
weather_data = []
with open("weather_data.csv", "r") as file:
    reader = csv.DictReader(file)
    for row in reader:
        weather_data.append(row)
        
        # Map phase
mapped_data = map(mapper, weather_data)

# Reduce phase
reduced_data = reduce(reducer, mapped_data, defaultdict(lambda: [0, 0]))

# Calculate average temperature for each year
avg_temp_per_year = {year: total_temp / count for year, (total_temp, count) in reduced_data.items()}

# Find coolest and hottest year
coolest_year = min(avg_temp_per_year.items(), key=lambda x: x[1])
hottest_year = max(avg_temp_per_year.items(), key=lambda x: x[1])

print("Coolest Year:", coolest_year[0], "Average Temperature:", coolest_year[1])
print("Hottest Year:", hottest_year[0], "Average Temperature:", hottest_year[1])
