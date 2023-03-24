import redis
from datetime import datetime
from time import sleep
import pandas as pd
from termcolor import colored, cprint
import subprocess


redis_client = redis.Redis()

test = "test"

#redis_client.set('test '+ test, test)

"""confirmed = 0
canseled = 0

confirmed_new = 0
canseled_new = 0
"""
def main():

    confirmed = 0
    canseled = 0

    confirmed_new = 0
    canseled_new = 0

    p = subprocess.Popen(['python', 'margin-process.py'])

    q = 0

    while True:
        sleep(150)
        #print(redis_client.keys())

        conf_keys = pd.DataFrame(redis_client.keys('conf*'))
        cans_keys = pd.DataFrame(redis_client.keys('cans*'))
        term_keys = pd.DataFrame(redis_client.keys('Term*'))

        #print(conf_keys)
        #print(cans_keys)

        confirmed = conf_keys.size
        canseled = cans_keys.size
        term = term_keys.size
        

        print(colored('Confirmed orders: ', 'white', 'on_yellow'), colored(confirmed, 'white', 'on_yellow'))
        print(colored('Canseled orders: ', 'white', 'on_yellow'), colored(canseled, 'white', 'on_yellow'))
        print(colored('Terminates ', 'white', 'on_yellow'), colored(term, 'white', 'on_yellow'))
        print(colored('q = ', 'white', 'on_yellow'), colored(q, 'white', 'on_yellow'))
        #print('Canseled orders: ', canseled)

        if confirmed > confirmed_new:
            confirmed_new = confirmed
            if q != 0:
                q -= 1
        else:
            q += 1

        if canseled > canseled_new:
            canseled_new = canseled
            if q != 0:
                q -= 1
        else:
            q += 1

        if q >= 4:
            print('q = ', q)
            q = 0
            cprint('Trminate!', 'white', 'on_yellow')
            p.terminate()
            redis_client.set('Terminates' + str(datetime.now()), str(datetime.now()))
            p = subprocess.Popen(['python', 'margin-process.py'])

if __name__ == '__main__':
    main()

redis_client.close()