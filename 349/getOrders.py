import websocket
import json
import time
import ccxt

key = "c97a7299646c0e447029850f0142b1f079f0d2e59440e7b7b134914de5a412f7"
secret = "83b80fdc33a9ea68426bc0ef2efb39b4b5c722890ca899a23db71ef0188b6308"
qtyrate = 200
# 构建 币安 平台
exchange = ccxt.binance({
    'apiKey': key,
    'secret': secret,
    'enableRateLimit': True,  # required https://github.com/ccxt/ccxt/wiki/Manual#rate-limit
    'options': {
        'defaultType': 'future',
    },
    'proxies': {
        'http': 'http://127.0.0.1:10809',  # no auth
        'https': 'http://127.0.0.1:10809',  # with auth
    },
})

if 'test' in exchange.urls:
    exchange.urls['api'] = exchange.urls['test']

markets = exchange.load_markets()
exchange.verbose = True
header = {
    "Accept-Encoding": "gzip, deflate, br",
    "Accept-Language": "zh-CN,zh;q=0.9,en;q=0.8",
    "Cache-Control": "no-cache",
    "Connection": "Upgrade",
    "Host": "349assistant.club",
    "Pragma": "no-cache",
    "Sec-WebSocket-Extensions": "permessage-deflate; client_max_window_bits",
    "Sec-WebSocket-Key": "PYAa9Mv056XzeA0SL2HFwg==",
    "Sec-WebSocket-Version": "13",
    "Upgrade": "websocket",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:90.0) Gecko/20100101 Firefox/90.0"
}


def on_ping(wsapp, message):
    print("[on_ping]:Got a ping!")


def on_pong(wsapp, message):
    # print("[on_pong]:Got a pong!")
    pass


def on_error(wsapp, err):
    print("[on_error]:Got an error:", err)


def on_close(ws, close_status_code, close_msg):
    print("[on_close]:closed")
    print("[on_close]:close_status_code", close_status_code)
    print("[on_close]:close_msg", close_msg)


def make_order(item: dict):
    """
    :param item:
    :return:
    """
    """
    349 消息类型
    开仓做多    {"avgPrice":1.741679,"direction":"BOTH","operDesc":"开仓做多","operationDesc":"(双向持仓)买入","orderId":3332723841,"orderTradeTime":1631153507348,"origQty":51840,"realFirmId":24,"shortTimeStr":"09-09 10:11","side":"BUY","symbol":"FTMUSDT","viewHis":"开","viewStyle":"kai"}
    多单加仓    {"avgPrice":11.453,"direction":"BOTH","operDesc":"多单加仓","operationDesc":"(双向持仓)买入","orderId":4007138054,"orderTradeTime":1631154203511,"origQty":6007,"realFirmId":24,"shortTimeStr":"09-09 10:23","side":"BUY","symbol":"NEARUSDT","viewHis":"加","viewStyle":"jia"}
    多单减仓    {"avgPrice":11.5,"direction":"BOTH","operDesc":"多单减仓","operationDesc":"(双向持仓)卖出","orderId":4007373589,"orderTradeTime":1631154539152,"origQty":6866,"realFirmId":24,"shortTimeStr":"09-09 10:28","side":"SELL","symbol":"NEARUSDT","viewHis":"减","viewStyle":"jian"}
    多单平仓    {"avgPrice":11.38,"direction":"BOTH","operDesc":"多单平仓","operationDesc":"(双向持仓)卖出","orderId":4007382871,"orderTradeTime":1631154549941,"origQty":6867,"realFirmId":24,"shortTimeStr":"09-09 10:29","side":"SELL","symbol":"NEARUSDT","viewHis":"平","viewStyle":"ping"}
    开仓做空    {"avgPrice":209.0152,"direction":"BOTH","operDesc":"开仓做空","operationDesc":"(双向持仓)卖出","orderId":4882791180,"orderTradeTime":1631157188417,"origQty":813,"realFirmId":24,"shortTimeStr":"09-09 11:13","side":"SELL","symbol":"SOLUSDT","viewHis":"开","viewStyle":"kai"}
    空单加仓    {"avgPrice":206.7689,"direction":"BOTH","operDesc":"空单加仓","operationDesc":"(双向持仓)卖出","orderId":4883181266,"orderTradeTime":1631157575540,"origQty":995,"realFirmId":24,"shortTimeStr":"09-09 11:19","side":"SELL","symbol":"SOLUSDT","viewHis":"加","viewStyle":"jia"}
    空单减仓    {"avgPrice":208.0694,"direction":"BOTH","operDesc":"空单减仓","operationDesc":"(双向持仓)买入","orderId":4883717962,"orderTradeTime":1631158146412,"origQty":498,"realFirmId":24,"shortTimeStr":"09-09 11:29","side":"BUY","symbol":"SOLUSDT","viewHis":"减","viewStyle":"jian"}
    买入平空    {"avgPrice":205.2972,"direction":"BOTH","operDesc":"买入平空","operationDesc":"(双向持仓)买入","orderId":4889305421,"orderTradeTime":1631163895160,"origQty":69,"realFirmId":24,"shortTimeStr":"09-09 13:04","side":"BUY","symbol":"SOLUSDT","viewHis":"平","viewStyle":"ping"} 
    """
    global exchange, qtyrate

    # 交易对
    symbol = exchange.markets_by_id[item["symbol"]]["symbol"]
    # 订单类型
    origType = 'MARKET'
    # 买卖方向
    side = item["side"]
    # 数量
    minqty = float(exchange.markets[symbol]['info']['filters'][1]['minQty'])
    quantity = float(item["origQty"]) / qtyrate
    quantity = max(
        float(exchange.amount_to_precision(symbol, quantity)), minqty)
    # 买卖方向
    if item["operDesc"] in ['开仓做多', '多单加仓', '多单减仓', '多单平仓']:
        positionSide = 'LONG'
    else:
        positionSide = 'SHORT'

    params = {
        "positionSide": positionSide
    }

    exchange.create_order(symbol=symbol, type=origType, side=side, amount=quantity, params=params)

def check_order():
    """
    检查当前持仓与349是否保持一致
    """
    pass


# 已经交易的订单号
orderIds = []

# 消息处理
# def on_message(wsapp, msg):


def on_message(msg):
    global orderIds

    data = json.loads(msg)

    if data['messageType'] == 'order':
        if data['orderRecord']['orderId'] not in orderIds:
            make_order(data['orderRecord'])
            orderIds.append(data['orderRecord']['orderId'])
    elif data['messageType'] == 'positions':
        check_order(data['positions'])


if __name__ == '__main__':
    print('CCXT Version:', ccxt.__version__)
    print("time:", time.ctime())

    msg = '{"messageType":"order","orderRecord":{"avgPrice":11.38,"direction":"BOTH","operDesc":"多单平仓","operationDesc":"(双向持仓)卖出","orderId":4007382871,"orderTradeTime":1631154549941,"origQty":10,"realFirmId":24,"shortTimeStr":"09-09 10:29","side":"SELL","symbol":"BTCUSDT","viewHis":"平","viewStyle":"ping"}  }'
    on_message(msg)

    # url = "wss://349assistant.club/websocket.ws/eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpc3MiOiIyOTU1IiwiZXhwIjoxNjMxNTE5OTQ2LCJpYXQiOjE2MzEyNjA3NDZ9.XdU30_DwVYFL80EyqLMiJr3U0k7dQWybW55fzPndbtY/24"
    # while True:
    #     try:
    #         wsapp = websocket.WebSocketApp(url=url,
    #                                        header=header,
    #                                        on_message=on_message,
    #                                        on_ping=on_ping,
    #                                        on_pong=on_pong,
    #                                        on_error=on_error,
    #                                        on_close=on_close,
    #                                        )

    #         wsapp.run_forever(origin="https://www.349assistant.com",
    #                           ping_interval=5, ping_timeout=1)
    #         wsapp.close()
    #     except Exception as e:
    #         print(Exception)
    #         wsapp.close()
