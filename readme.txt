Home Electricity Trading Estimator based on NordPool prices

Note

The creation of this code and documentation heavily utilized OpenAI's ChatGPT. While the algorithm's output has been sanity-checked, the code itself has not undergone rigorous testing.

Overview

This project estimates the potential earnings a private homeowner in Estonia could achieve by leveraging a home battery. The idea is to buy and store electricity when prices are low and sell it back to the grid when prices are high. By analyzing real-time electricity market prices, a homeowner can make informed decisions on the optimal times to buy and sell electricity. This could serve as a ballpark model for those considering investments in home energy storage solutions. IMPORTANT: Electricity is obtained only from the grid, NOT FROM SOLAR. If you want to emulate solar, you can change the buying price to 0 in the code, but that is not perfect as the code has no consideration for day/night nor season and you can't likely charge a full 14kwh within one hour in most cases. On some days you wont be able to make any money as the 20% VAT and 3c fee eat into your earnings too much. 2018 had only a few days you could actually make some money.

Source of Data
The electricity prices are sourced from Elering's Dashboard https://dashboard.elering.ee/en

Assumptions

The capacity of the home battery is 14 kWh.
You want to sell electricity no later than 12h after buying it (6-12h was empirically tested to be the most profitable time window as it is long enough to find a greatly higher price for selling, yet short enough to maximise selling cycles)
The prices fetched are in euros per MWH, and the program converts them to cents per KWH.
When selling back to the grid, the homeowner faces a VAT of 20% and a net-connection tariff of 3 cents per kWh.

Pseudocode Description

The code attempts to find the maximum price difference within a 12-hour window (max_window = 12). Specifically, it's looking for pairs of times within this window where:

The earlier time has a price that, when increased by a margin of 20% (representing VAT) and an added net-connection tariff of 3 cents per kWh, is maximally lower than the later time's price.
It starts by considering the price at the current time index i and checks against every subsequent price up to 12 hours (max_window) ahead.
If it finds a time pair with the maximum difference in this rolling window, it logs that difference, calculates potential earnings based on selling 14 kWh of electricity at that price difference, and then skips ahead to the time of the higher price to begin the next search.
If no such pair is found in the current window, the code will move the starting time index i ahead by one and repeat the process.
In simpler terms, it's trying to identify times when buying electricity (considering VAT and a net-connection tariff) would be the cheapest and selling it would be the most profitable within a 12-hour period, with the aim to maximize profit from selling a stored 14 kWh of electricity.
