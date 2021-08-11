import ccxt
import config

exchange = ccxt.binance()
if exchange:
    exchange.apiKey = config.apiKey
    exchange.secret = config.secret
    exchange.proxies = {
        'http': 'http://127.0.0.1:10809',
        'https': 'http://127.0.0.1:10809'
    }

print(exchange.fapiPrivateGetPositionSideDual())
