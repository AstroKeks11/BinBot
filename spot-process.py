from time import sleep

from binance.client import Client
import pandas as pd
from binance.enums import *
from termcolor import colored, cprint
import redis

import key
import functions as f

client =  Client(key.key, key.secretKey)

symbol = 'BTCUSDT'
pause = 1

redis_client = redis.Redis()

def main():

    cash = f.USDT_balance()
    if cash < 10:
        print('Недостаточно средств!')
        redis_client.set('Low_balance', 'low balance')
    else:

        quantity = f.all_tickers()

        buy_price = f.bids_price()

        id_buy = f.order_buy(quantity, buy_price)

        buy_status = f.check_spot(id_buy)

        q = 0
        while (buy_status != 'ok') and (q != 3):
            sleep(pause)
            sleep(pause)
            print('Cycle: ', q)
            q += 1
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
                    cprint('WIN!!!', 'white', 'on_green')
                    redis_client.set('confirmed '+ str(sell_price), buy_price)
                    main()
        elif buy_status == 'not ok':
            cansel = f.cansel_spot_order(id_buy)
            if cansel == 'ok':
                #print('Cansel order. Price:', buy_price, ', Id:', id_buy )
                print(colored('Cansel order. Price:', 'white', 'on_red'), colored(buy_price, 'white', 'on_red'), colored(', Id:', 'white', 'on_red'), colored(id_buy, 'white', 'on_red') )
                redis_client.set('cansel '+ str(id_buy), buy_price)
                main()

            elif cansel == 'error':
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
                    cprint('WIN!!!', 'white', 'on_green')
                    redis_client.set('confirmed '+ str(sell_price), buy_price)

                    
        


if __name__ == '__main__':
    main()