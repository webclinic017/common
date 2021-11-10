import requests
import time
import random
import logging

# LOG_FORMAT = "%(asctime)s - %(levelname)s - %(message)s"
# DATE_FORMAT = "%m/%d/%Y %H:%M:%S %p"
# logging.basicConfig(filename='my.log', level=logging.INFO, format=LOG_FORMAT, datefmt=DATE_FORMAT)

url = "https://www.binancezh.top/bapi/futures/v1/public/future/leaderboard/getOtherPosition"

data = {"encryptedUid": "D9DBFAC2D9B25C1293B03C041A42F249",
        "tradeType": "PERPETUAL"}

proxy = {
    'http': 'http://127.0.0.1:10809',
    'https': 'http://127.0.0.1:10809'
}

headers = {
    "Host": 'www.binancezh.top',
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:92.0) Gecko/20100101 Firefox/92.0",
    "Accept": "*/*",
    "Accept-Language": "zh-CN,zh;q=0.8,zh-TW;q=0.7,zh-HK;q=0.5,en-US;q=0.3,en;q=0.2",
    "Accept-Encoding": "gzip, deflate, br",
    "Content-Type": "application/json",
    "lang": "zh-CN",
}

while True:
    response = requests.post(url=url, json=data, headers=headers, proxies=proxy)
    # logging.info("[" + str(time.time() * 1000) + "]==>" + response.content.decode())
    print("[" + str(time.time() * 1000) + "]==>" + response.content.decode())
    time.sleep(0.5)
