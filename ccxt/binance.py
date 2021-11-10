import ccxt
print('CCXT Version:', ccxt.__version__)
exchange = ccxt.binance({
    'enableRateLimit': True,
    'apiKey': 'c97a7299646c0e447029850f0142b1f079f0d2e59440e7b7b134914de5a412f7',
    'secret': '83b80fdc33a9ea68426bc0ef2efb39b4b5c722890ca899a23db71ef0188b6308',
    'options': { 'defaultType': 'future' },
    'proxies' : {
        'http': 'http://127.0.0.1:10809',
        'https': 'http://127.0.0.1:10809'
    }
})

exchange.set_sandbox_mode(True)

markets = exchange.load_markets()

exchange.verbose = True

balance = exchange.fetch_balance()