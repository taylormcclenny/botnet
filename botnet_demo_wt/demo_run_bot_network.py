

import config
import requests, time, subprocess
from binance.client import Client


my_coins_list = ['BTC', 'ETH']
coins_to_alert_list = ['BTC', 'ETH']


RSI_BUY_THRESHOLD_1d = 100
RSI_BUY_THRESHOLD_1h = 100
RSI_BUY_THRESHOLD_15m = 100


client = Client(config.API_KEY, config.API_SECRET, tld='us')

ta_indicator = "rsi"
intervals = ['1d', '1h', '15m']

endpoint = "https://api.taapi.io/{}".format(ta_indicator)


### Helpers
pair_to_alert_list_usd = []
for coin in coins_to_alert_list:
    pair_to_alert_list_usd.append(f"{coin}USD")  # For formatting w/ & w/o "USD"


def run_bot_network():

    all_coin_pairs_tickers = client.get_all_tickers()  # Gets most recent, most accurate tickers
    # pprint.pprint(all_coin_pairs_tickers)

    for coin_pairs in all_coin_pairs_tickers:

        if coin_pairs['symbol'] in pair_to_alert_list_usd:

            coin_usd = coin_pairs['symbol']                  # "BTC", "BTCUSD", "BTCUSDT" ...
            current_market_price = float(coin_pairs['price'])

            # Prepare for Technical Analysis Request
            coin = coin_usd.split('USD', 1)[0]
            rsi_list = []

            for interval in intervals:
                parameters = {
                    'secret': config.TA_SECRET,
                    'exchange': 'binance',
                    'symbol': f"{coin}/USDT",        # Insert coin trading pair symbol
                    'interval': interval        # Insert 'interval' times
                    }
                try:
                    response = requests.get(url=endpoint, params=parameters)
                    result = response.json()
                    rsi = round(result['value'], 2)
                    # print(f'{coin} {interval} {rsi}')
                    rsi_list.append(rsi)
                except Exception as e:
                    print(f'ERROR: {e}')

            print(f"{coin_usd} //  $ {current_market_price} - RSI LIST: {rsi_list}")

            # Sleep - Restarting loop...
            time.sleep(1.5)     # To avoid too many/too fast API calls

            
            if rsi_list[0] < RSI_BUY_THRESHOLD_1d and rsi_list[1] < RSI_BUY_THRESHOLD_1h and rsi_list[2] < RSI_BUY_THRESHOLD_15m:

                print(f"Buying Conditions met for {coin_usd}!  Checking for Coin & Order Status...")

                # Trigger Market Alert
                '''
                try:
                    if condition_meet:
                        alerts.send_email(message, comm.taylor_email_list)
                except Exception as e:
                    print(f'ERROR: {e}')
                '''

                # If this is a coin I trade, open a new deal, if not already in an Active Deal
                if coin in my_coins_list:

                    # Get Active Deals - To check if there is already an Active Deal for this Coin 
                    # AND/OR if we're already at Max Number of Deals
                    '''
                    active_deals = deals.get_active_deals()
                    '''
                    
                    # Open NEW Deal if not already in Active Deal
                    '''
                    if coin_usd not in active_deals and len(active_deals) < MAX_DEALS:
                    '''

                    #### OPEN New Active Deal
                    try:
                        bot_script = "simple_fake_dca_bot.py"
                        process_string = f"venv/bin/python3 {bot_script} BUY {coin_usd}"
                        subprocess.Popen(process_string, shell=True)
                        print(f"Running System Command:  '{process_string}'")

                        #### Update Deal to ACTIVE - Add to Active Deals JSON
                        '''
                        new_deal = {f"{coin_usd}" : [
                                                    {
                                                    "bot_type" : f"{demo_comm.BOT_TYPE}", 
                                                    "datetime" : f"{datetime.now()}", 
                                                    "side" : "BUY"
                                                    }]
                                    }
                        deals.append_active_deals(new_deal)   # Append Active Trade log for limiting multiple active trades per coin
                        '''
                    except Exception as e:
                        print(f'ERROR: {e}')






if __name__ == '__main__':

    run_bot_network()