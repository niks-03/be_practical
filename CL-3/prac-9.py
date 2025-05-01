import csv
from collections import defaultdict

def process_weather_data(file_path):
    # Read and process data in one go
    yearly_temps = defaultdict(lambda: [0, 0])
    
    with open(file_path, "r") as file:
        for row in csv.DictReader(file):
            year = row["day"].split("-")[0]
            temp = float(row["temperature"])
            yearly_temps[year][0] += temp
            yearly_temps[year][1] += 1
    
    # Calculate averages and find extremes
    avg_temps = {year: total/count for year, (total, count) in yearly_temps.items()}
    coolest = min(avg_temps.items(), key=lambda x: x[1])
    hottest = max(avg_temps.items(), key=lambda x: x[1])
    
    return coolest, hottest

if __name__ == "__main__":
    file_path = "E:\\Nikhil\\8th sem lab ass\\cl-3\\weather_data.csv"
    coolest, hottest = process_weather_data(file_path)
    print(f"Coolest Year: {coolest[0]}, Average Temperature: {coolest[1]:.2f}")
    print(f"Hottest Year: {hottest[0]}, Average Temperature: {hottest[1]:.2f}")