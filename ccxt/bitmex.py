import ccxt
import json
import time

bitmex = ccxt.bitmex()
if 'test' in bitmex.urls:
    bitmex.urls['api'] = bitmex.urls['test']
    bitmex.apiKey = 'MKNlfeopzaI318muF2ohKwMT'
    bitmex.secret = 'b2DM__fG1MCY563N6-XRwY0i98sxIFDuIwwHQyi-DtsYeZyf'
    bitmex.proxies = {
        'http': 'http://127.0.0.1:10809',
        'https': 'http://127.0.0.1:10809'
    }

# print(json.dumps(bitmex.load_markets()['BTC/USD'], indent=4))
bitmex.load_markets()
print(json.dumps(bitmex.fetch_order_book('BTC/USD'), indent=4))
