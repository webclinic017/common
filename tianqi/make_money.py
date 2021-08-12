import asyncio
from datetime import datetime
import time as tim
from aiowebsocket.converses import AioWebSocket
import json
from ccxt.binance import binance
import jsonpath
import deal
# from utils import readKey, saveDB, saveFile

single = 0  # 重启变量

async def fetch_data(uri, header):
    async with AioWebSocket(uri, union_header=header, timeout=1000) as aws:
        converse = aws.manipulator
        message = '{"op":"init"}'

        # 消息剔除重复用
        message_bytes_unique = 'message_bytes_unique'.encode('utf-8')

        await converse.send(message)
        
        #实例化交易所
        binance = deal.Exchange()

        while True:
            #存活信息打印
            if (int(tim.strftime("%M")) % 15 == 0 and int(tim.strftime("%S")) <= 3):  # 大约15分钟记录1次
                print("[{time}] I'm alive!".format(time=datetime.now().strftime('%Y-%m-%d %H:%M:%S')))
                # saveFile.saveToTxt('logs/TraderT.err',
                #                    "[{time}] I'm alive!\n".format(time=datetime.now().strftime('%Y-%m-%d %H:%M:%S')))

            # 接收收据
            message_bytes_new = await converse.receive()
            # message_bytes = '{"op":"orderListResult","isUpdate":true,"data":{"binanceApiId":100017,"name":"TraderT","exchange":"binance","itemCount":12399,"itemList":[{"binanceApiId":100017,"orderId":28197161293,"symbol":"BTCUSDT","status":"NEW","clientOrderId":"ios_VXj7nqKaJeYt7IcBzu3z","price":"45863.45","avgPrice":"0","origQty":"2","executedQty":"0","timeInForce":"GTC","type":"NEW","reduceOnly":false,"closePosition":false,"side":"SELL","positionSide":"SHORT","stopPrice":"0","workingType":"CONTRACT_PRICE","origType":"LIMIT","time":1628522031824,"updateTime":1628522031824,"origPositionAmt":-23.377,"totalExecutedQty":0,"totalAvgPrice":0},{"binanceApiId":100017,"orderId":1138081385,"symbol":"ALICEUSDT","status":"FILLED","clientOrderId":"ios_vmRaChuilR9ZiEITitv0","price":"0","avgPrice":"11.9507","origQty":"10000","executedQty":"10000","timeInForce":"GTC","type":"TRADE","reduceOnly":true,"closePosition":false,"side":"SELL","positionSide":"LONG","stopPrice":"0","workingType":"CONTRACT_PRICE","origType":"MARKET","time":1628521491171,"updateTime":1628521491171,"origPositionAmt":21645.1,"totalExecutedQty":10000,"totalAvgPrice":11.9507},{"binanceApiId":100017,"orderId":8389765504235739000,"symbol":"ETHUSDT","status":"FILLED","clientOrderId":"ios_O4P6hpZFtSgtsA7hxpBh","price":"3129.80","avgPrice":"3129.95000","origQty":"1.500","executedQty":"1.500","timeInForce":"GTC","type":"TRADE","reduceOnly":false,"closePosition":false,"side":"SELL","positionSide":"SHORT","stopPrice":"0","workingType":"CONTRACT_PRICE","origType":"LIMIT","time":1628520063128,"updateTime":1628520063128,"origPositionAmt":-318,"totalExecutedQty":1.5,"totalAvgPrice":3129.95},{"binanceApiId":100017,"orderId":28179123845,"symbol":"BTCUSDT","status":"FILLED","clientOrderId":"ios_Zn7H58KlnJxXjw68t7ro","price":"45959","avgPrice":"45959","origQty":"1.500","executedQty":"1.500","timeInForce":"GTC","type":"TRADE","reduceOnly":false,"closePosition":false,"side":"SELL","positionSide":"SHORT","stopPrice":"0","workingType":"CONTRACT_PRICE","origType":"LIMIT","time":1628510057679,"updateTime":1628510057679,"origPositionAmt":-21.877,"totalExecutedQty":1.5,"totalAvgPrice":45959},{"binanceApiId":100017,"status":"LEVERAGE","side":"LEVERAGE","symbol":"BTCUSDT","oldLeverage":25,"leverage":20,"orderId":1628508570937.2,"clientOrderId":"16285085709370.3","price":0,"avgPrice":0,"origQty":0,"executedQty":0,"timeInForce":0,"type":"","positionSide":"","stopPrice":0,"workingType":"","origType":"","time":1628508570937,"updateTime":1628508570937,"origPositionAmt":0},{"binanceApiId":100017,"orderId":8389765504220274000,"symbol":"ETHUSDT","status":"FILLED","clientOrderId":"ios_CxzXTCuM250ZV54dllZv","price":"3138.49","avgPrice":"3138.49836","origQty":"18","executedQty":"18","timeInForce":"GTC","type":"TRADE","reduceOnly":false,"closePosition":false,"side":"SELL","positionSide":"SHORT","stopPrice":"0","workingType":"CONTRACT_PRICE","origType":"LIMIT","time":1628508364277,"updateTime":1628508364277,"origPositionAmt":-300,"totalExecutedQty":18,"totalAvgPrice":3138.49836},{"binanceApiId":100017,"orderId":8389765504220164000,"symbol":"ETHUSDT","status":"FILLED","clientOrderId":"ios_XvVWY1aUpjnnR7lJownb","price":"3133.31","avgPrice":"3133.61795","origQty":"20","executedQty":"20","timeInForce":"GTC","type":"TRADE","reduceOnly":false,"closePosition":false,"side":"SELL","positionSide":"SHORT","stopPrice":"0","workingType":"CONTRACT_PRICE","origType":"LIMIT","time":1628508289861,"updateTime":1628508289861,"origPositionAmt":-280,"totalExecutedQty":20,"totalAvgPrice":3133.61795},{"binanceApiId":100017,"orderId":8389765504219046000,"symbol":"ETHUSDT","status":"FILLED","clientOrderId":"ios_TUVidoQxn56GXdTfVPvy","price":"3132.16","avgPrice":"3132.16000","origQty":"80","executedQty":"80","timeInForce":"GTC","type":"TRADE","reduceOnly":false,"closePosition":false,"side":"SELL","positionSide":"SHORT","stopPrice":"0","workingType":"CONTRACT_PRICE","origType":"LIMIT","time":1628507536804,"updateTime":1628507536804,"origPositionAmt":-200,"totalExecutedQty":80,"totalAvgPrice":3132.16},{"binanceApiId":100017,"orderId":8389765504217773000,"symbol":"ETHUSDT","status":"FILLED","clientOrderId":"ios_FTqkGxrocKEyVISQTwgN","price":"3105.91","avgPrice":"3106.89277","origQty":"20","executedQty":"20","timeInForce":"GTC","type":"TRADE","reduceOnly":false,"closePosition":false,"side":"SELL","positionSide":"SHORT","stopPrice":"0","workingType":"CONTRACT_PRICE","origType":"LIMIT","time":1628506822315,"updateTime":1628506822315,"origPositionAmt":-180,"totalExecutedQty":20,"totalAvgPrice":3106.89277},{"binanceApiId":100017,"orderId":28173737873,"symbol":"BTCUSDT","status":"FILLED","clientOrderId":"ios_vy08nvqS1pRcRGPxXYyG","price":"45680.65","avgPrice":"45690.23015","origQty":"3.700","executedQty":"3.700","timeInForce":"GTC","type":"TRADE","reduceOnly":false,"closePosition":false,"side":"SELL","positionSide":"SHORT","stopPrice":"0","workingType":"CONTRACT_PRICE","origType":"LIMIT","time":1628506809715,"updateTime":1628506809715,"origPositionAmt":-18.177,"totalExecutedQty":3.7,"totalAvgPrice":45690.23015}]}}'

            # 判断是否下单数据,转字符串为了模糊匹配
            message_str = str(message_bytes_new)
            if message_str.find('orderListResult') != -1 and message_str.find('TraderT') != -1:

                # 下单数据重复推送，只解析第1次推送的
                if (message_bytes_new != message_bytes_unique):
                    message_bytes_unique = message_bytes_new

                    # 字节转json
                    jsonobj = json.loads(message_bytes_new)

                    time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                    operator = jsonpath.jsonpath(jsonobj, '$.data.name')[0]
                    exchange = jsonpath.jsonpath(jsonobj, '$.data.exchange')[0]
                    id = jsonpath.jsonpath(jsonobj, '$.data.itemCount')[0]
                    rec = jsonpath.jsonpath(jsonobj, '$.data.itemList[0]')[0]
                    symbol = jsonpath.jsonpath(jsonobj, '$..symbol')[0]
                    type = jsonpath.jsonpath(jsonobj, '$..type')[0]
                    status = jsonpath.jsonpath(jsonobj, '$..status')[0]
                    side = jsonpath.jsonpath(jsonobj, '$..side')[0]
                    positionSide = jsonpath.jsonpath(jsonobj, '$..positionSide')[0]
                    price = jsonpath.jsonpath(jsonobj, '$..price')[0]
                    amount = jsonpath.jsonpath(jsonobj, '$..executedQty')[0]
                    
                    # ******************************* 1、下单 *******************************
                    # 暂时以市价跟随以成功下单的交易
                    if status == 'FILLED':
                        #转成ccxt识别的symbol
                        symbol = symbol.replace('USDT','/USDT')
                        binance.create_order(symbol=symbol, type='market', side=side, amount=amount/50, positionSide=positionSide)
                    

                    # ******************************* 2、打印 *******************************
                    # print(jsonpath.jsonpath(jsonobj,'$.data.itemCount'))
                    print('[{time}]  {operator} {exchange} {id} {rec}\n'
                          .format(time=time, operator=operator, exchange=exchange, id=id, rec=rec))

                    # # ******************************* 2、写文件 *******************************
                    # saveFile.saveToTxt('logs/TraderT.order', '[{time}] {operator} {exchange} {id} {rec}\n'
                    #                    .format(time=time, operator=operator, exchange=exchange, id=id, rec=rec))

                    # saveFile.saveToTxt('logs/TraderT.log', '[{time}] {operator} {exchange} {id} {mes}\n'
                    #                    .format(time=time, operator=operator, exchange=exchange, id=id,
                    #                            mes=message_bytes_new.decode('utf-8')))

                    # # ******************************* 3、存入数据库 *******************************
                    # saveDB.saveToMySQL(message_bytes_new)


def start_up():
    # SecWebSocketKey = readKey.readline('conf/SecWebSocketKey.txt')  # header中的socketkey，需定期更换
    # print('SecWebSocketKey:', SecWebSocketKey)

    remote = 'wss://hk.tianqi.one/'
    header = {"Pragma": "no-cache",
              "Origin": "https://www.tianqi.one",
              "Accept-Language": "zh-CN,zh;q=0.9,en;q=0.8",
              "Sec-WebSocket-Key": "HPmW+1vP7l8r+vF3QU/YAw==",
            #   "Sec-WebSocket-Key": SecWebSocketKey,
              "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML:like Gecko) Chrome/91.0.4472.164 Safari/537.36",
              "Upgrade": "websocket",
              "Sec-WebSocket-Extensions": "permessage-deflate; client_max_window_bits",
              "Cache-Control": "no-cache",
              "Sec-WebSocket-Protocol": "bm",
              "Connection": "Upgrade",
              "Sec-WebSocket-Version": "13"
              }
    try:
        asyncio.get_event_loop().run_until_complete(fetch_data(remote, header))
    except Exception as e:
        print("[{time}]出现如下异常：{e}\n".format(time=datetime.now().strftime('%Y-%m-%d %H:%M:%S'), e=e))
        # saveFile.saveToTxt('logs/TraderT.err',
        #                    "[{time}] 出现如下异常：{e}\n".format(time=datetime.now().strftime('%Y-%m-%d %H:%M:%S'), e=e))
        single = 0


if __name__ == '__main__':
    print('[{time}]：启动！\n'.format(time=datetime.now().strftime('%Y-%m-%d %H:%M:%S')))
    # saveFile.saveToTxt('logs/TraderT.err', '[{time}]：启动！\n'.format(time=datetime.now().strftime('%Y-%m-%d %H:%M:%S')))

    while True:
        if single == 0:
            start_up()
            print('[{time}]：重连成功！\n'.format(time=datetime.now().strftime('%Y-%m-%d %H:%M:%S')))
            # saveFile.saveToTxt('logs/TraderT.err',
            #                    '[{time}]：重连成功！\n'.format(time=datetime.now().strftime('%Y-%m-%d %H:%M:%S')))
