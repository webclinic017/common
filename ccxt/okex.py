import ccxt
import config

exchange = ccxt.okex5()

if exchange:
    exchange.urls['api'] = exchange.urls['test']
    exchange.apiKey = config.apiKey
    exchange.secret = config.secret
    exchange.password = config.password
    exchange.proxies = {
        'http': 'http://127.0.0.1:10809',
        'https': 'http://127.0.0.1:10809'
    }
    
print(exchange.fetch_balance())