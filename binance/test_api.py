# from binance.client import Client
# import json

# apiKey = 'c97a7299646c0e447029850f0142b1f079f0d2e59440e7b7b134914de5a412f7'
# secret = '83b80fdc33a9ea68426bc0ef2efb39b4b5c722890ca899a23db71ef0188b6308'
# proxies = {
#     'http': 'http://127.0.0.1:10809',
#     'https': 'http://127.0.0.1:10809'
# }

# client = Client(apiKey, secret, {'proxies' : proxies, "type" : "future"}, testnet=True)

# res = client.get_order('BTCUSDT', )

# print(json.dumps(res, indent=4))

import random
import time

print(time.time()*1000)