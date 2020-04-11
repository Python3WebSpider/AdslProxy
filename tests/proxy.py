from adslproxy import RedisClient

client = RedisClient(host='', password='')
random = client.random()
all = client.all()
names = client.names()
proxies = client.proxies()
count = client.count()

print('RANDOM:', random)
print('ALL:', all)
print('NAMES:', names)
print('PROXIES:', proxies)
print('COUNT:', count)
