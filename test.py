import time

import redis

redis_client = redis.Redis()


"""
redis_client.set('counter',1)

while True:
    redis_client.incr('counter')
    time.sleep(1)

redis_client.close()"""

redis_client.set('val', 'ttt1')

answer = redis_client.get('val')
print(answer)

print(redis_client.keys())
print(redis_client.keys("*l"))
redis_client.close()