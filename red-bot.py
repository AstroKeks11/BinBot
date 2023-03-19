import redis



redis_client = redis.Redis()

redis_client.set('key', 2)

print(redis_client.get('key'))

print(redis_client.keys())

redis_client.close()