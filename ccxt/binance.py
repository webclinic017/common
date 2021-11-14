import ccxt
import json

print('CCXT Version:', ccxt.__version__)
exchange = ccxt.binance({
    'enableRateLimit': True,
    'apiKey': 'wERNL9AGH4LG97MS6cghG8ZCSpMfPR76vbKGfr5Nj5zQL3EAZQlmqbTbXeV5kZrT',
    'secret': 'a9YnhCDYnSCTToUwcl9km5f1n0n0Ai9ma5N9BTw6dGwfcWcUpszimy4rfTkRyRTK',
    'options': { 'defaultType': 'future' },
    'proxies' : {
        'http': 'http://127.0.0.1:10809',
        'https': 'http://127.0.0.1:10809'
    }
})

# exchange.set_sandbox_mode(True)
def format_josn_data(recv_msg):
    print(json.dumps(recv_msg, indent=4))
    
exchange.load_markets()

# format_josn_data(exchange.fetch_open_orders('OMG/USDT'))
# exchange.set_margin_mode()

# print(json.dumps(exchange.fetch_open_orders('LTC/USDT'), indent=4))
# print(exchange.markets_by_id["BTCUSDT"]["symbol"])
exchange.create_order(symbol='IOTX/USDT', type='MARKET', side='BUY', amount=500, price=0, params={"positionSide": "SHORT","quantity": 500,})