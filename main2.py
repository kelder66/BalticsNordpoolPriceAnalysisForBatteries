import csv
import os
from datetime import datetime
from math import ceil


# Read the relevant data from the CSV file
def read_csv(filename):
    with open(filename, encoding='latin-1') as csvfile:
        csvreader = csv.reader(csvfile, delimiter=';')
        next(csvreader)
        
        prices = []
        for row in csvreader:
            try:
                date_time = row[1]
                # Converting euros per MWH to cents per KWH
                price = float(row[-1].replace(',', '.')) * 100 / 1000
                prices.append((date_time, price))
            except ValueError:
                continue
                
    return prices

# Analyze the prices
def analyze_prices(prices):
    max_window = 12  # 12-hour window
    i = 0
    total_money_made = 0.0
    total_electricity_sold = 0
    total_profitable_cycles = 0
    
    while i < len(prices) - max_window:
        max_diff = 0.0
        pair = None
        for start in range(i, i + max_window):
            for j in range(start + 1, start + max_window):
                if j >= len(prices):
                    break
                
                #diff = prices[j][1] - (prices[start][1]*1.2+3) # add vat and 3c net-connection tariff per kwh
                #diff = prices[j][1] - (prices[start][1]) # test without vat and net-connection tariff
                diff = prices[j][1] # test in the case you get energy for free, i.e Solar
                if diff > max_diff:
                    max_diff = diff
                    pair = (start, j)
        
        if pair is not None:
            money_made = 14 * max_diff  # 14 KWH * max difference in cents
            total_money_made += money_made
            total_profitable_cycles += 1 
            total_electricity_sold += 14 # Assuming 14 KWH is sold
            i = pair[1] + 1  # Move to the time index of the higher price to begin the next search
        else:
            i += 1
    
    total_money_made = ceil(total_money_made / 100)  # Convert cents to euros and round up
    
    # Analyzing the time period and number of days
    start_time = datetime.strptime(prices[0][0], "%d.%m.%Y %H:%M")
    end_time = datetime.strptime(prices[-1][0], "%d.%m.%Y %H:%M")
    num_days = (end_time - start_time).days
    
    return total_money_made, total_electricity_sold, total_profitable_cycles, start_time, end_time, num_days

# Output summary
def output_summary(filename, analysis_results):
    total_money_made, total_electricity_sold, total_profitable_cycles, start_time, end_time, num_days = analysis_results
    print(f"\nFilename: {filename}")
    print(f"Total money made: {total_money_made} euros")
    print(f"Total electricity sold: {total_electricity_sold} KWH")
    print(f"Total profitable cycles: {total_profitable_cycles}")
    print(f"Time period analyzed: from {start_time} to {end_time}, {num_days} days")

# Iterating over all the .csv files in the current directory
for filename in os.listdir():
    if filename.endswith(".csv"):
        estonia_prices = read_csv(filename)
        analysis_results = analyze_prices(estonia_prices)
        output_summary(filename, analysis_results)
