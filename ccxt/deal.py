import ccxt

class Exchange():

    def __init__(self) -> None:
        self.binance = ccxt.binance()
        if 'test' in self.binance.urls:
            self.binance.urls['api'] = self.binance.urls['test']
            self.binance.apiKey = 'c97a7299646c0e447029850f0142b1f079f0d2e59440e7b7b134914de5a412f7'
            self.binance.secret = '83b80fdc33a9ea68426bc0ef2efb39b4b5c722890ca899a23db71ef0188b6308'
            self.binance.proxies = {
                'http': 'http://127.0.0.1:10809',
                'https': 'http://127.0.0.1:10809'
            }

    def create_order(self, symbol, type, side, amount):
        self.binance.create_order(symbol=symbol, type=type,side=side, amount=amount, params={"type": "future"})
