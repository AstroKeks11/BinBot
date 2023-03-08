from binance import Client, ThreadedWebsocketManager, ThreadedDepthCacheManager
from binance.exceptions import BinanceAPIException
from time import sleep
import pandas as pd
from datetime import datetime
import key

'''
Программа для автоматической спотовой торговли на Binance
Представляет из себя набор функций, которые вызывают друг друга поочередно
Нет никакой стратегии или индикаторов - вся торговля происходит по рынку: первая функция находит наиболее привлекательную цену в стакане
(цену, для которой на данный момент имеется наибольший объем спроса) и размещает ордер на покупку
После его срабатывания вызывается функция, ищущая в стакане цену для продажи и создается ордер по этой цене.
После его срабатывания снова запускается поиск цены на покупку.
Главный минус - если рынок резко уйдет вниз, ордер на продажу зависает вместе с "котлетой", и
программа будет ждать его срабатывания 

3.1 Добавлен запрос время и его запись в историю, доработана строчка расчета колличества валюты для торговли

На данном этапе нужно отработать ошибки, уменьшить или искуственно ограничить колличество запросов,
добавить колораму

'''


apikey = key.apikey
secret = key.secret
client = Client(apikey, secret)

symbol = 'BTCUSDT'

file_name = symbol+'.txt'
file = open(file_name, 'a')     #Открываем файл для записи истории ордеров

tickers = client.get_all_tickers()
ticker_df = pd.DataFrame(tickers)
ticker_df.set_index('symbol', inplace = True)   #Меняем тип вывода всех тикеров, что бы было проще к ним обращаться

quantity = round((15/float(ticker_df.loc[symbol]['price'])), 5) #Первая цифра в скобках - колличество валюты для торговли
#quantity = 0.0006 #Можно использовать эту строчку вместо предыдущей, самому выставляя колличество

my_price = 0
my_price2 = 0

def bids_price():
    depth = client.get_order_book(symbol = symbol)
    bids = depth['bids']                #Запрашиваем все ордера торгуемой пары. Выбираем из них те, что на покупку

    bids_amount = []
    bids_price = []
    i = 1
    p = 0
    while i <= 100:
        bids_amount.append(float(bids[p][1]))  #Из списка всех позиций и цен (100) создаем два списка
        bids_price.append(float(bids[p][0]))
        i += 1
        p += 1

    print('Всего BTC на покупку: ' + str(sum(bids_amount)))
    print('Наибольшее колличество BTC на покупку: ' + str(max(bids_amount)))

    index = bids_amount.index(max(bids_amount)) #Находим индекс, принадлежащий самой крупной позиции в списке

    print('Место: ' + str(index))
    print('Цена: ' + str(bids_price[index]))
    print('Проверка: ' + str(bids[index]))
    my_price = bids_price[index]
    return order_buy(bids_price[index])

def order_buy(price):
    try:
        order = client.order_limit_buy(
                    symbol=symbol,
                    quantity=quantity,
                    price=price)
    except BinanceAPIException:
        print('Сумма ордера превышает сумму средств на балансе!')
    print('Создался ордер на покупку')
    my_price = price
    return check_buy2(price)

def check_buy2(price):
    q =1
    orders = client.get_open_orders(symbol=symbol)  #Запрашиваем открытые ордера
    while orders != []:                             #Если их нет, то значит что ордер сработал
        orders = client.get_open_orders(symbol=symbol)
        print('Ждем пока купится ' + str(q))
        q += 1                                      #Если одер на покупку не срабатывает, то отменяем его и занова 
        if q == 50:                                 #и снова запрашиваем цену
            orders = client.get_open_orders(symbol=symbol)
            try:
                last_order = orders[0]['orderId']
            except IndexError:          #Ошибка происходит еслипытаемся взять информацию из пустого списка, 
                print('Error')          #в случае если ордер сработал одновременно с запросом
                print('Ордер на покупку сработал')
                raw_server_time = client.get_server_time()
                server_time = datetime.fromtimestamp(raw_server_time['serverTime']/1000.0).replace(microsecond=0)
                file.write(str(server_time) + ' Куплено ' + str(quantity) + ' ' + str(symbol) + ' по ' + str(price))
                return asks_price(price)
            result = client.cancel_order(
                symbol=symbol,
                orderId=last_order)
            print('Ордер отменен')
            return bids_price()
    if orders == []:
        print('Ордер на покупку сработал')
        raw_server_time = client.get_server_time()
        server_time = datetime.fromtimestamp(raw_server_time['serverTime']/1000.0).replace(microsecond=0)
        file.write(str(server_time) + ' Куплено ' + str(quantity) + ' ' + str(symbol) + ' по ' + str(price))
        return asks_price(price)

def asks_price(price):
    depth = client.get_order_book(symbol = symbol)
    asks = depth['asks']

    asks_amount = []
    asks_price = []
    i1 = 1
    p1 = 0
    while i1 <= 100:
        asks_amount.append(float(asks[p1][1]))
        asks_price.append(float(asks[p1][0]))
        i1 += 1
        p1 += 1

    print('Всего BTC на продажу: ' + str(sum(asks_amount)))
    print('Наибольшее колличество BTC на продажу: ' + str(max(asks_amount)))

    index1 = asks_amount.index(max(asks_amount))

    print('Место: ' + str(index1))
    print('Цена: ' + str(asks_price[index1]))
    print('Проверка: ' + str(asks[index1]))
    try:
        if price < asks_price[index1]:
            return order_sell(asks_price[index1])
        else:
            asks_price(price)
    except TypeError:
        if price < asks_price[index1]:
            return order_sell(asks_price[index1])
        else:
            asks_price(price)

def order_sell(price):
    order = client.order_limit_sell(
                symbol=symbol,
                quantity=quantity,
                price=price)
    print('Создался ордер на продажу')
    return check_sell2(price)

def check_sell2(price):
    w = 0
    orders = client.get_open_orders(symbol=symbol)
    while orders != []:
        orders = client.get_open_orders(symbol=symbol)
        print('Ждем пока продастся ' + str(w))
        w += 1
        if w == 1000:
            sleep(40)
            w = 0
    if orders == []:
        file.write(' Продано по ' + str(price) + '\n')
        print('YOU WIN!')
        return bids_price()

bids_price()
