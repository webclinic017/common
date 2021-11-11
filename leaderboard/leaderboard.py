import json
import requests
import time
import datetime
import ccxt
import csv
import copy

# key
key = "c97a7299646c0e447029850f0142b1f079f0d2e59440e7b7b134914de5a412f7"
secret = "83b80fdc33a9ea68426bc0ef2efb39b4b5c722890ca899a23db71ef0188b6308"

# 交易员
person = {"name": "TraderT",
          "encryptedUid": "CCF3E0CB0AAD54D9D6B4CEC5E3E741D2", "tradeType": "PERPETUAL"}
# 比例
qtyrate = 1000

DEBUG = True

# 构建 币安 平台
exchange = ccxt.binance({
    'apiKey': key,
    'secret': secret,
    'enableRateLimit': True,
    'options': {'defaultType': 'future'},
    'proxies': {
        'http': 'http://127.0.0.1:10809',
        'https': 'http://127.0.0.1:10809'
    }
})

if DEBUG:
    exchange.set_sandbox_mode(True)

markets = exchange.load_markets()
# exchange.verbose = True

# 排行榜链接
urls = ["https://www.binancezh.top/bapi/futures/v1/public/future/leaderboard/getOtherPosition", ]


# 不同币种滑动比例
lossRate = {
    'BTCUSDT': 1, 'ETHUSDT': 1,
}
lossLimitNum = 5

firstrate = 0.015  # 第一次, 限价单亏损比例
secrate = 0.065  # 第二次, 限价单亏损比例

csvheaders = ['time', 'symol', 'position',
              'side', 'operate', 'quantity', "price"]
csv_f = open('%s.csv' % (person["name"]), 'a+', newline='')
csv_w = csv.DictWriter(csv_f, csvheaders)
csv_w.writeheader()
csv_f.flush()

headers = {
    # "Host": "www.binance.com",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:93.0) Gecko/20100101 Firefox/93.0",
    # "Accept": "*/*",
    # "Accept-Language": "zh-CN,zh;q=0.8,zh-TW;q=0.7,zh-HK;q=0.5,en-US;q=0.3,en;q=0.2",
    # "Content-Type": "application/json",
    # "lang": "zh-CN",
    # "Pragma": "no-cache",
    # "Cache-Control": "no-cache",
    # "Origin": "https://www.binance.com",
    # "Sec-Fetch-Dest": "empty",
    # "Sec-Fetch-Mode": "cors",
    # "Sec-Fetch-Site": "same-origin",
    # "Connection": "keep-alive",
}


# 打印列表
def printlist(list):
    print("<><><><><>")
    for item in list:
        print(item)
    print("<><><><><>")


# 获取 订单信息
def getjson():
    num = 0
    while True:
        try:
            req = requests.post(url=urls[0], json=person, headers=headers)
            json = req.json()["data"]["otherPositionRetList"]
            return json
        except Exception as e:
            num = num + 1
            if num > 10:
                exit(0)
            if DEBUG:
                text = req.text
                print("Except:", text)
                
# 开仓、加仓
def openprocess(nowdict, openflag=True):
    # 判断是加仓还是开仓
    openstr = "开仓" if openflag else "加仓"
    sym = exchange.markets_by_id[nowdict["symbol"]]["symbol"]
    minqty = max(float(6 / nowdict["entryPrice"]), float(exchange.markets[sym]['info']['filters'][1]['minQty']))
    minqty = float(exchange.amount_to_precision(sym, abs(minqty)))

    ori_qty = float(nowdict["amount"])
    if (ori_qty > 0):
        side = "BUY"
        position = "LONG"
    else:
        side = "SELL"
        position = "SHORT"
    price = float(exchange.price_to_precision(sym, nowdict["entryPrice"]))
    print("\n##### ##### leaderboard start(%s) ##### #####" % openstr)
    temptime = datetime.datetime.now()
    print("nowdict", nowdict)
    print("交易员:%s\t" % person["name"], 
          "orderType:%s\t" % openstr,
          "symbol:%s\t" % (sym),
          "position:%s\t" % (position),
          "side:%s\t" % (side),
          "quantity:%.5f\t" % (ori_qty),
          "price:%.5f\t" % (price),
          "time:%s" % (temptime)
          )
    row = {"symol": sym, 'time': temptime, 'position': position, 'side': side, 'quantity': ori_qty, "price": price, "operate": "open"}
    csv_w.writerow(row)
    csv_f.flush()
    # 市价单部分
    ori_pri = price
    qty = ori_qty / qtyrate / 4
    qty = max(float(exchange.amount_to_precision(sym, abs(qty))), minqty)
    params = {
        "positionSide": position,
        "quantity": qty,
    }
    order = exchange.create_order(sym, "MARKET", side, qty, ori_pri, params)
    ret = order["info"]

    print("order:", ret)
    t_str = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(int(ret["updateTime"]) / 1000))
    print("%s \t 市价成交 %s %s \t %s \t 均价:%s \t 数量:%s \t 种类:%s" % (t_str, ret["side"], ret["positionSide"], ret["origType"], ret["avgPrice"], ret["origQty"], ret["symbol"]))

    # 限价单部分
    # 以交易员的成交价挂单
    qty = ori_qty / qtyrate / 4
    qty = max(float(exchange.amount_to_precision(sym, abs(qty))), minqty)
    params = {
        "positionSide": position,
        "quantity": qty,
    }
    exchange.create_order(sym, "LIMIT", side, qty, price, params=params)
    print("%s \t 限价挂单 %s %s \t %s \t 均价:%s \t 数量:%s \t 种类:%s" % (t_str, side, params["positionSide"], 'LIMIT', price, qty, sym))
    # 以设置的允许下跌区间分批挂单
    qty = ori_qty / qtyrate / 4 * 2 / lossLimitNum
    qty = max(float(exchange.amount_to_precision(sym, abs(qty))), minqty)
    params = {
        "positionSide": position,
        "quantity": qty,
    }
    for index in range(1, lossLimitNum + 1):
        if side == "BUY":
            price = float(exchange.price_to_precision(sym, ori_pri * (1 - lossRate.get(sym,2) / lossLimitNum / 100 * index)))
        else:
            price = float(exchange.price_to_precision(sym, ori_pri * (1 + lossRate.get(sym,2) / lossLimitNum / 100 * index)))
        exchange.create_order(sym, "LIMIT", side, qty, price, params=params)
        print("%s \t 限价挂单 %s %s \t %s \t 均价:%s \t 数量:%s \t 种类:%s" % (t_str, side, params["positionSide"], 'LIMIT', price, qty, sym))

    print("##### ##### leaderboard end (%s) ##### #####" % openstr)
    
# 平仓
def closeprocess(olddict):
    sym = exchange.markets_by_id[olddict["symbol"]]["symbol"]
    minqty = float(exchange.markets[sym]['info']['filters'][1]['minQty'])

    ori_qty = -float(olddict["amount"])

    if (ori_qty > 0):
        side = "BUY"
        position = "SHORT"
    else:
        side = "SELL"
        position = "LONG"
    price = float(exchange.price_to_precision(sym, olddict["markPrice"]))
    print("\n##### ##### leaderboard start(清仓) ##### #####")
    temptime = datetime.datetime.now()
    print("olddict", olddict)
    print("order:close\t",
          "symbol:%s\t" % (sym),
          "position:%s\t" % (position),
          "side:%s\t" % (side),
          "quantity:%.5f\t" % (ori_qty),
          "price:%.5f\t" % (price),
          "time:%s" % (temptime)
          )
    row = {"symol": sym, 'time': temptime, 'position': position, 'side': side, 'quantity': ori_qty, "price": price, "operate": "close"}
    csv_w.writerow(row)
    csv_f.flush()
    params = {
        "positionSide": position,
        "quantity": abs(ori_qty)
    }
    order = exchange.create_order(sym, "MARKET", side, abs(ori_qty), params=params)
    ret = order["info"]

    print("order:", ret)
    t_str = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(int(ret["updateTime"]) / 1000))
    print("%s \t %s %s \t %s \t 均价:%s \t 数量:%s \t 种类:%s" % (t_str, ret["side"], ret["positionSide"], ret["origType"], ret["avgPrice"], ret["origQty"], ret["symbol"]))
    # 限价单取消
    orders = exchange.fetch_open_orders(sym)
    for order in orders:
        exchange.cancel_order(order['id'], sym)
        print("==>cancel :%s \t symbol:%s\t amount:%s \t price:%s" % (order['id'], order['symbol'], order["remaining"], order["price"]))
        
    print("##### ##### leaderboard end (清仓) ##### #####")
                
# 加减仓
def modifyprocess(nowdict, olddict):
    '''
        加减仓策略:
            1、如果是加仓，将加仓的数量计算出来，调用开仓逻辑
            2、如果是减仓，查询当前持仓，按交易员减仓比例平仓
    '''
    global exchange
    now_sym = nowdict["symbol"]
    now_qty = nowdict["amount"]
    now_prc = nowdict["entryPrice"]
    old_qty = olddict["amount"]
    
    # 判断加仓还是减仓
    if (abs(now_qty) > abs(old_qty)):
        ori_qty = now_qty - old_qty
        nowdict["amount"] = ori_qty
        openprocess(nowdict, False)
    else:
        sym = exchange.markets_by_id[now_sym]["symbol"]
        minqty = float(exchange.markets[sym]['info']['filters'][1]['minQty'])
        ori_qty = now_qty - old_qty
        if (ori_qty > 0):
            side = "BUY"
        else:
            side = "SELL"
        if (old_qty > 0):
            position = "LONG"
        else:
            position = "SHORT"
        price = float(exchange.price_to_precision(sym, now_prc))
        print("\n##### ##### leaderboard start(减仓) ##### #####")
        temptime = datetime.datetime.now()
        print("nowdict", nowdict)
        print("olddict", olddict)
        print("交易员:%s\t" % person["name"],
            "orderType:减仓\t",
            "symbol:%s\t" % (sym),
            "position:%s\t" % (position),
            "side:%s\t" % (side),
            "quantity:%.5f\t" % (abs(ori_qty)),
            "price:%.5f\t" % (price),
            "time:%s" % (temptime)
            )
        row = {"symol": sym, 'time': temptime, 'position': position, 'side': side, 'quantity': abs(ori_qty), "price": price, "operate": "减仓"}
        csv_w.writerow(row)
        csv_f.flush()
        # 查询当前持仓
        my_positions = exchange.fetch_positions(symbols=sym)
        for p in my_positions:
            if p["info"]["positionSide"] == position:
                myqty = float(p["info"]["positionAmt"])
        act_qty = max(float(exchange.amount_to_precision(sym, abs(ori_qty) / abs(old_qty) * abs(myqty))), minqty)
        params = {
            "positionSide": position,
            "quantity": act_qty,
        }
        order = exchange.create_order(sym, "MARKET", side, act_qty, price, params=params)
        ret = order["info"]
        print("order:", ret)
        t_str = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(int(ret["updateTime"]) / 1000))
        print("%s \t %s %s \t %s \t 均价:%s \t 数量:%s \t 种类:%s" % (t_str, ret["side"], ret["positionSide"], ret["origType"], ret["avgPrice"], ret["origQty"], ret["symbol"]))
        print("##### ##### leaderboard end(减仓) ##### #####")

def delta_data(nowdata, olddata):
    global exchange, qtyrate
    tempdata = copy.deepcopy(olddata)

    for nowdict in nowdata:
        # 区分是要修改还是开仓
        sameflag = False
        # 新字典内容
        nowsym = nowdict["symbol"]
        nowqty = nowdict["amount"]
        price = nowdict["entryPrice"]
        # print("nowdict", nowdict)
        for index, olddict in enumerate(tempdata):
            if olddict == None:
                continue
            oldsym = olddict["symbol"]
            oldqty = olddict["amount"]
            # print("olddict", olddict)

            if (nowsym == oldsym and nowqty * oldqty > 0):
                # print("same")
                sameflag = True
                tempdata[index] = None
                sym = exchange.markets_by_id[nowsym]["symbol"]
                minqty = float(exchange.markets[sym]['info']['filters'][1]['minQty'])
                if (abs(nowqty - oldqty) > minqty * 4 * qtyrate and abs(nowqty - oldqty) * price > 6 * 4 * qtyrate):
                    # 加减仓
                    try:
                        modifyprocess(nowdict, olddict)
                    except Exception as e:
                        print("modifyprocess failed", e)
                break

        # 开仓
        if sameflag == False:
            try:
                openprocess(nowdict)
            except Exception as e:
                print("openprocess failed", e)

    # 清仓
    for index, olddict in enumerate(tempdata):
        if olddict == None:
            continue
        try:
            closeprocess(olddict)
        except Exception as e:
            print("closeprocess failed", e)
            
if __name__ == '__main__':    
    
    print(person["name"])

    oldtime = time.time() * 1000

    olddata = getjson()
    # printlist(olddata)
    while (True):
        # time.sleep(0.1)
        nowdata = getjson()
        try:
            delta_data(nowdata, olddata)
        except ccxt.ExchangeError as e:
            print("ExchangeError:", e)
        except Exception as e:
            print("Except:", e)
        olddata = nowdata.copy()
