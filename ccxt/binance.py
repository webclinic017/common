import ccxt
import json
import jsonpath
import deal

binance = ccxt.binance()
if 'test' in binance.urls:
    binance.urls['api'] = binance.urls['test']
    binance.apiKey = 'c97a7299646c0e447029850f0142b1f079f0d2e59440e7b7b134914de5a412f7'
    binance.secret = '83b80fdc33a9ea68426bc0ef2efb39b4b5c722890ca899a23db71ef0188b6308'
    binance.proxies = {
        'http': 'http://127.0.0.1:10809',
        'https': 'http://127.0.0.1:10809'
    }
    
binance.create_order(symbol='BTC/USDT', type='market', side='buy', amount=5, params={"type": "future", "positionSide" : 'LONG'})
