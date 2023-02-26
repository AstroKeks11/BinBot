import redis

# Create a Redis client
redis_host = 'redis'
redis_port = 6379
redis_client = redis.Redis(host='localhost', port=redis_port)


# Set a key in Redis
redis_client.set('my_key', 'my_value')

# Get a value from Redis
value = redis_client.get('my_key')
print(value)