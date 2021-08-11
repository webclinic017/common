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

bitmex.load_markets()

# print(json.dumps(bitmex.load_markets()['BTC/USD'], indent=4))
# orderbook = bitmex.fetch_order_book('BTC/USD')
# bid = orderbook['bids'][0][0] if len (orderbook['bids']) > 0 else None
# ask = orderbook['asks'][0][0] if len (orderbook['asks']) > 0 else None
# spread = (ask - bid) if (bid and ask) else None
# print (bitmex.id, 'market price', { 'bid': bid, 'ask': ask, 'spread': spread })

# print(json.dumps(bitmex.fetch_ticker('BTC/USD'), indent=4))

# print(bitmex.fetch_balance())

# print(bitmex.fetch_orders(symbol='BTC/USD'))

# print(bitmex.fetch_trades(symbol='BTC/USD'))
if bitmex.has['fetchOpenOrders']:
    print(bitmex.fetchClosedOrders(symbol='BTC/USD'))
