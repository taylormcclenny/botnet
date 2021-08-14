

import config
import sys, time
from binance.client import Client


#######################
### RUN BOT NETWORK ###
#######################

''' 1. Set Process Inputs to Variables
    2. Create Binance US Client Connection
    3. Simulate Opening New Deal - Print that we're entering a Fake New Deal (Buy Order)
    4. Begin Deal Monitoring While Loop
        a. If Deal Closed (Sell Order Filled), Update DB, End Bot Process
        b. Else Check Coin's Current Market Price & Check Order Statuses for Coin; Sleep 1.5s
'''

# Set Process Inputs to Variables
SIDE = sys.argv[1]
COIN_USD = sys.argv[2].upper()
TICKER_SLEEP_TIME = 1.5

# Create Client config for connection
client = Client(config.API_KEY, config.API_SECRET, tld='us')

# Fake New Order Notice
print(f"\n\nNew Deal Opened on {COIN_USD}!\n")


###################################
### COIN & DEAL MONITORING LOOP ###
###################################

deal_is_complete = False
counter = 0
while deal_is_complete == False:

    if counter > 5:   # TESTING!!! - For when deal is done

        # WHEN THE DEAL IS DONE - Remove Coin from Active Deals & Close the Process
        # Fake Closed Deal Order Notice
        print(f"\nClose Deal on {COIN_USD}!\n")

        # End the process
        sys.exit()

    else:

        # Check Coin Pair Ticker Current Market Price & All Orders for Coin Pair every 1.5 seconds
        all_coins = client.get_all_tickers()
        for coin in all_coins:
            if coin['symbol'] == COIN_USD:
                symbol = coin['symbol']
                current_market_price = float(coin['price'])
                print(f"   Monitoring... // {symbol} //  Current Market Price ${current_market_price}\n")

                # Check All Orders for Coin Pair (not the best/final way to do this...)
                all_orders = client.get_all_orders(symbol=COIN_USD, recvWindow=60000)  # <- It's breaking here

        # Sleep - Restarting loop...
        time.sleep(TICKER_SLEEP_TIME)

    counter+=1
