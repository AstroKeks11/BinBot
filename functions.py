from time import sleep

import key
from binance.client import Client
from binance.exceptions import BinanceAPIException
import pandas as pd
from binance.enums import *
#from binance import AsyncClient
#import asyncio
from termcolor import colored, cprint


client =  Client(key.key, key.secretKey)

symbol = 'BTCUSDT'
pause = 1

def main():
    price = client.get_ticker(symbol=symbol)['lastPrice']
    print('BTC: ', price)

    quantity = all_tickers()

    #order_buy(quantity)

    balance()

    margin_info = client.get_margin_account()
    print('Margin info:')
    assets = margin_info['userAssets']
    for asset in assets:
        if asset['asset'] == 'USDT':
            print('Свободных маржинальных USDT: ', asset['free'])
    #print(assets)

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
    asks_price()
    """
    order = client.get_margin_order(
    symbol=symbol,
    orderId=19273093874)
    print(order['status'])
    """

    def order_test():
        order = client.create_margin_order(
            symbol=symbol,
            side=SIDE_BUY,
            type=ORDER_TYPE_LIMIT,
            timeInForce=TIME_IN_FORCE_GTC,
            quantity=0.0005,
            price='21000')  

        print(order)

        if order['fills'] == []:
            print('Ничего нет')
        return order['orderId']

    orderId = order_test()

    def check_test(orderId):
        order = client.get_margin_order(
        symbol=symbol,
        orderId=orderId)  #Узнаем статус маржинального ордера

        print(order)

    check_test(orderId)

    def cansel_test(orderId):
        result = client.cancel_margin_order(
            symbol=symbol,
            orderId=orderId)
        
    cansel_test(orderId)
    print('cansel')

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

    quantity = round((10.5/float(ticker_df.loc[symbol]['price'])), 5)
    print('quantity: ', quantity)
    return quantity


def balance():
    BTC_balance = client.get_asset_balance(asset='BTC')
    print('BTC balance: ', BTC_balance['free'])

    USDT_balance = client.get_asset_balance(asset='USDT')
    print('USDT balance: ', USDT_balance['free'])

    BNB_balance = client.get_asset_balance(asset='BNB')
    print('BNB balance: ', BNB_balance['free'])

def USDT_balance():
    USDT_balance = client.get_asset_balance(asset='USDT')
    #return float(USDT_balance)
    return float(USDT_balance['free'])


def USDT_margin_balance():
    margin_info = client.get_margin_account()
    assets = margin_info['userAssets']
    for asset in assets:
        if asset['asset'] == 'USDT':
            #print('Свободных маржинальных USDT: ', asset['free'])
            return float(asset['free'])


def trades():
    trades = client.get_my_trades(symbol=symbol)
    print(trades[0]) #Последняя сделка


def orders():
    orders = client.get_open_orders()
    print('Открытые спотовые ордеры: ')
    print(orders)   #Все открытые ордера
    #print(orders[0]['orderId']) 

    print('Открытые маржинальные ордеры: ')
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
    #print(max_bids)
    bids_price = max_bids['Price'].values[0] #Выбираем из строки цену
    print('Bids Price: ', bids_price)
    return bids_price

def asks_price():       #Как bids_price, но для ордеров на продажу
    depth = client.get_order_book(symbol = symbol)
    asks_df = pd.DataFrame(depth['asks'])
    asks_df.columns = ['Price', 'Amount']
    max_amount = asks_df['Amount'].max()
    max_asks = asks_df[asks_df['Amount']==max_amount]
    asks_price = max_asks['Price'].values[0]
    print('Asks Price: ', asks_price)
    pr = (float(asks_price)/100)*0.15
    asks_price = round((float(asks_price) + pr),2)
    print(str(asks_price))
    return str(asks_price)


def order_buy(quantity, price):
    order = client.order_limit_buy(
        symbol=symbol,
        quantity=quantity,
        price=price)  #Размещение спотового лимитного ордера на покупку
    order_ID = order['orderId']
    return order_ID
    

def order_sell(quantity, price):
    order = client.order_limit_sell(
        symbol=symbol,
        quantity=quantity,
        price=price)  #Размещение спотового лимитного ордера на продажу
    
    order_ID = order['orderId']
    return order_ID
    

def order_margin_buy(quantity, price):
    order = client.create_margin_order(
    symbol=symbol,
    side=SIDE_BUY,
    type=ORDER_TYPE_LIMIT,
    timeInForce=TIME_IN_FORCE_GTC,
    quantity=quantity,
    price=price)  #Размещение маржинального лимитного ордера на покупку

    order_ID = order['orderId']
    return order_ID


def order_margin_sell(quantity, price):
    order = client.create_margin_order(
    symbol=symbol,
    side=SIDE_SELL,
    type=ORDER_TYPE_LIMIT,
    timeInForce=TIME_IN_FORCE_GTC,
    quantity=quantity,
    price=price)  #Размещение маржинального лимитного ордера на продажу

    order_ID = order['orderId']
    return order_ID


def check_spot(orderId):
    order = client.get_order(
    symbol=symbol,
    orderId=orderId)  #Узнаем статус спотового ордера

    status = order['status']
    if status != 'FILLED':
        sleep(pause)
        check_spot(orderId)
    elif status == 'FILLED':
        return 'ok'



def check_marg(orderId):
    order = client.get_margin_order(
    symbol=symbol,
    orderId=orderId)  #Узнаем статус маржинального ордера

    status = order['status']
    if status != 'FILLED':
        return 'not ok'
    elif status == 'FILLED':
        return 'ok'
""" 
def check_marg_buy_cansel(orderId):
    order = client.get_margin_order(
    symbol=symbol,
    orderId=orderId)  #Узнаем статус маржинального ордера

    if order['status'] == 'FILLED':
        return 'ok'
    elif (order['status'] != 'FILLED') and (order['executedQty'] == '0'):
        sleep(pause)
        order = client.get_margin_order(
        symbol=symbol,
        orderId=orderId)

        if order['status'] == 'FILLED':
            return 'ok'
        else:
            result = client.cancel_margin_order(
                symbol=symbol,
                orderId=orderId)
"""        
def cansel_marg_order(orderId):
    try:
        result = client.cancel_margin_order(
            symbol=symbol,
            orderId=orderId)
        return 'ok'
    except BinanceAPIException: 
        #print('error')
        cprint('ERROR', 'white', 'on_red')
        return 'error'
        
def cansei_spot_order(orderID):
    try:
        result = client.cancel_order(
            symbol=symbol,
            orderId=orderID)
        return 'ok'
    except BinanceAPIException:
        cprint('ERROR', 'white', 'on_red')
        return 'error'

### Main ###

if __name__ == '__main__':
    main()