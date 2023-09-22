import csv
from datetime import datetime
from math import ceil

# Read the relevant data from the CSV file
def read_csv(filename):
    with open(filename, encoding='latin-1') as csvfile:
        csvreader = csv.reader(csvfile, delimiter=';')
        header = next(csvreader)

        prices = []
        for row in csvreader:
            try:
                date_time = row[1]
                price = float(row[-1].replace(',', '.'))
                # Convert to cents per KWH
                price = price * 100 / 1000
                prices.append((date_time, price))
            except ValueError:
                continue

    return prices

# Analyze the prices to find the pair with maximal difference
def analyze_prices(prices):
    max_window = 12  # 12-hour window
    money_by_month = {}  # To store money made by month
    total_electricity_sold = 0  # In KWH

    i = 0
    while i < len(prices) - 1:
        max_diff = 0.0
        pair = None

        # Look for a maximum within the 12-hour window
        for j in range(i + 1, min(i + max_window, len(prices))):
            diff = prices[i][1] - prices[j][1]

            if diff > max_diff:
                max_diff = diff
                pair = (i, j)

        if pair is not None:
            i1, i2 = pair
            dt1, p1 = prices[i1]
            dt2, p2 = prices[i2]

            # Extract month and year from dt1
            month_year = datetime.strptime(dt1, "%d.%m.%Y %H:%M").strftime("%Y-%m")

            # Calculate money made with 14 KWH at max_diff
            money_made = 14 * max_diff
            money_by_month.setdefault(month_year, 0)
            money_by_month[month_year] += money_made

            total_electricity_sold += 14

            i = i2 + 1  # Move to the position of the second element + 1
        else:
            i += 1  # Move one slot forward if no pair is found

    # Convert to euros and round up to the nearest full euro
    money_by_month = {k: ceil(v / 100) for k, v in money_by_month.items()}
    
    print("Money made by month:", money_by_month)
    print(f"Total electricity sold: {total_electricity_sold} KWH")

    start_time = datetime.strptime(prices[0][0], "%d.%m.%Y %H:%M")
    end_time = datetime.strptime(prices[-1][0], "%d.%m.%Y %H:%M")
    days = (end_time - start_time).days

    print(f"Data analyzed from {start_time} to {end_time} ({days} days)")

# Read the data
filename = 'electricity-nps price_20230921-5.csv'
estonia_prices = read_csv(filename)

# Analyze the data
analyze_prices(estonia_prices)
