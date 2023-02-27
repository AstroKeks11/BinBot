from time import sleep

from binance.client import Client
import pandas as pd
from binance.enums import *

import key
import functions as f

client =  Client(key.key, key.secretKey)

symbol = 'BTCUSDT'
pause = 1

def main():

    cash = f.USDT_balance()
    if cash < 10:
        print('Недостаточно средств!')
    else:

        quantity = f.all_tickers()

        buy_price = f.bids_price()

        id_buy = f.order_buy(quantity, buy_price)

        buy_status = f.check_spot(id_buy)
        while buy_status != 'ok':
            sleep(pause)
            sleep(pause)
            buy_status = f.check_spot(id_buy)

        if buy_status == 'ok':
            sell_price = f.asks_price()

            while sell_price < buy_price:
                sleep(pause)
                sell_price = f.asks_price()
            
            if sell_price > buy_price:
                id_sell = f.order_sell(quantity, sell_price)

                sell_status = f.check_spot(id_sell)
                while sell_status != 'ok':
                    sleep(pause)
                    sleep(pause)
                    sell_status = f.check_spot(id_sell)

                if sell_status == 'ok':
                    print('WIN!!!')

                    main()
                    
        


if __name__ == '__main__':
    main()