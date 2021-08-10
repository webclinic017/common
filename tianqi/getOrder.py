import asyncio
from datetime import datetime
import time
from aiowebsocket.converses import AioWebSocket

single = 0

async def fetch_data(uri, header):
    async with AioWebSocket(uri, union_header=header, timeout=1000) as aws:
        converse = aws.manipulator
        message = '{"op":"init"}'
        await converse.send(message)
        while True:
            mes = await converse.receive()
            # if str(mes).find('"isUpdate":true') != -1:
            if str(mes).find('"isUpdate":false') != -1:
                print('{time}-Client receive: {rec}'
                      .format(time=datetime.now().strftime('%Y-%m-%d %H:%M:%S'), rec=str(mes)[0:50]))


def start_up():
    remote = 'wss://hk.tianqi.one/'
    header = {"Pragma": "no-cache",
              "Origin": "https://www.tianqi.one",
              "Accept-Language": "zh-CN,zh;q=0.9,en;q=0.8",
              "Sec-WebSocket-Key": "9c9bFnDJJTJjL/ItR6cwrw==",
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
        print(e)
        single = 1


if __name__ == '__main__':
    
    start_up()
    
    while True:
        if single == 1:
            start_up()
            print('{time}-Client : 重连成功'
                  .format(time=datetime.now().strftime('%Y-%m-%d %H:%M:%S')))
