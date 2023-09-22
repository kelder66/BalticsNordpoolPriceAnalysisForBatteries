import csv
from datetime import datetime
from math import ceil

# Read the relevant data from the CSV file
def read_csv(filename):
    print("Reading CSV data...")
    with open(filename, encoding='latin-1') as csvfile:
        csvreader = csv.reader(csvfile, delimiter=';')
        header = next(csvreader)
        
        prices = []
        for row in csvreader:
            try:
                date_time = row[1]
                # Converting euros per MWH to cents per KWH
                price = float(row[-1].replace(',', '.')) * 100 / 1000
                prices.append((date_time, price))
            except ValueError:
                continue
                
    print("Finished reading CSV data.")
    return prices

# Analyze the prices
def analyze_prices(prices):
    print("Starting to analyze prices...")
    
    max_window = 12  # 12-hour window
    i = 0
    total_money_made = 0.0
    total_electricity_sold = 0
    
    while i < len(prices) - max_window:
        max_diff = 0.0
        pair = None
        for start in range(i, i + max_window):
            for j in range(start + 1, start + max_window):
                if j >= len(prices):
                    break
                
                diff = prices[j][1] - (prices[start][1]*1.2+3) # add vat and 3c net-connection tariff per kwh
                #diff = prices[j][1] - 0 #experiment with 0 cost solar power
                if diff > max_diff:
                    max_diff = diff
                    pair = (start, j)
        
        if pair is not None:
            start, end = pair
            dt_start, price_start = prices[start]
            dt_end, price_end = prices[end]
            print(f"Max difference found between {dt_start} and {dt_end}: {max_diff} cents")
            
            money_made = 14 * max_diff  # 14 KWH * max difference in cents
            total_money_made += money_made
            total_electricity_sold += 14  # Assuming 14 KWH is sold
            
            print(f"Money made in this window: {money_made} cents")
            
            i = end + 1
        else:
            i += 1
    
    total_money_made = ceil(total_money_made / 100)  # Convert cents to euros and round up
    print(f"Total money made: {total_money_made} euros")
    print(f"Total electricity sold: {total_electricity_sold} KWH")
    
    # Analyzing the time period and number of days
    start_time = datetime.strptime(prices[0][0], "%d.%m.%Y %H:%M")
    end_time = datetime.strptime(prices[-1][0], "%d.%m.%Y %H:%M")
    num_days = (end_time - start_time).days
    
    print(f"Time period analyzed: from {start_time} to {end_time}, {num_days} days")
    
# Read the data
filename = 'electricity-nps price_20230921-4.csv'
estonia_prices = read_csv(filename)

# Analyze the data
analyze_prices(estonia_prices)
