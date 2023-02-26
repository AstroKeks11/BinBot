import time

import key
from binance.client import Client
import pandas as pd
from binance.enums import *
#from binance import AsyncClient
#import asyncio


client =  Client(key.key, key.secretKey)

symbol = 'BTCUSDT'

def main():
    price = client.get_ticker(symbol=symbol)['lastPrice']
    print('BTC: ', price)

    quantity = all_tickers()

    #order_buy(quantity)

    balance()

    trades()
    """def op_or():
        order = client.create_margin_order(
        symbol='BTCUSDT',
        side=SIDE_SELL,
        type=ORDER_TYPE_LIMIT,
        timeInForce=TIME_IN_FORCE_GTC,
        quantity=0.0005,
        price='30000')
        print(order['orderId'])

    op_or()
    """
    orders()

    bids_price()
    """
    order = client.get_margin_order(
    symbol=symbol,
    orderId=19273093874)
    print(order['status'])
    """

    print('ok')
    i = input('Введите что-то:  ')
    print(i)

### Functions ###

def all_tickers():
    tickers = client.get_all_tickers()
    ticker_df = pd.DataFrame(tickers)
    #ticker_df.to_csv('test.csv')
    #ticker_df.to_json('test.json')
    ticker_df.set_index('symbol', inplace = True)
    #print(ticker_df)

    print('BTC: ', ticker_df.loc[symbol]['price'])

    quantity = round((10.1/float(ticker_df.loc[symbol]['price'])), 5)
    print('quantity: ', quantity)
    return quantity


def balance():
    BTC_balance = client.get_asset_balance(asset='BTC')
    print('BTC balance: ', BTC_balance['free'])

    USDT_balance = client.get_asset_balance(asset='USDT')
    print('USDT balance: ', USDT_balance['free'])

    BNB_balance = client.get_asset_balance(asset='BNB')
    print('BNB balance: ', BNB_balance['free'])


def trades():
    trades = client.get_my_trades(symbol=symbol)
    print(trades[0]) #Последняя сделка


def orders():
    orders = client.get_open_orders()
    print(orders)   #Все открытые ордера
    #print(orders[0]['orderId']) 
    orders = client.get_open_margin_orders(symbol=symbol)
    print(orders) #Все открытые маржинальные ордеры


def bids_price():
    depth = client.get_order_book(symbol = symbol) #Все ставки на symbol, "глубина стакана"
    bids_df = pd.DataFrame(depth['bids'])
    bids_df.columns = ['Price', 'Amount']
    #print(bids_df)
    max_amount = bids_df['Amount'].max()
    #print(max_amount)
    max_bids = bids_df[bids_df['Amount']==max_amount] #Находим строку с наибольшим колличеством symbol для покупки
    print(max_bids)
    bids_price = max_bids['Price'].values[0] #Выбираем из строки цену
    print('Price: ', bids_price)
    return bids_price


def order_buy(quantity, price):
    order = client.order_limit_buy(
        symbol=symbol,
        quantity=quantity,
        price=price)  #Размещение спотового лимитного ордера на покупку
    order_ID = order['orderId']
    

def order_sell(quantity, price):
    order = client.order_limit_sell(
        symbol=symbol,
        quantity=quantity,
        price=price)  #Размещение спотового лимитного ордера на продажу
    
    order_ID = order['orderId']
    

def order_margin_buy(quantity, price):
    order = client.create_margin_order(
    symbol=symbol,
    side=SIDE_BUY,
    type=ORDER_TYPE_LIMIT,
    timeInForce=TIME_IN_FORCE_GTC,
    quantity=quantity,
    price=price)  #Размещение маржинального лимитного ордера на покупку

    order_ID = order['orderId']


def order_margin_buy(quantity, price):
    order = client.create_margin_order(
    symbol=symbol,
    side=SIDE_SELL,
    type=ORDER_TYPE_LIMIT,
    timeInForce=TIME_IN_FORCE_GTC,
    quantity=quantity,
    price=price)  #Размещение маржинального лимитного ордера на продажу

    order_ID = order['orderId']


def check_spot(orderId):
    order = client.get_order(
    symbol=symbol,
    orderId=orderId)  #Узнаем статус спотового ордера

    status = order['status']


def check_marg(orderId):
    order = client.get_margin_order(
    symbol=symbol,
    orderId=orderId)  #Узнаем статус маржинального ордера

    status = order['status']


### Main ###

if __name__ == '__main__':
    main()