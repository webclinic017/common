import time
import hmac
import hashlib
import requests

apiKey = 'XZkZC8NUV6q0sYiUXvVDuC3bju8ZbdljS2LuKIVxOedLjosGPkvRaIIF4HHA9kwz'
apiSecretKey = '3vsd2kW8Zw1fKxb7hxRl9YI6E1V9VWeS4vb47gj9SfotLC9N3cKnvjtB0fmbxDjx'
apiKey_test = 'c97a7299646c0e447029850f0142b1f079f0d2e59440e7b7b134914de5a412f7'
apiSecretKey_test = '83b80fdc33a9ea68426bc0ef2efb39b4b5c722890ca899a23db71ef0188b6308'

proxies = {
    'http': 'http://127.0.0.1:10809',
    'https': 'http://127.0.0.1:10809'
}

baseUrl = 'https://fapi.binance.com'
baseUrl_test = 'https://testnet.binancefuture.com'

coin_list = ['BTC', 'LTC', 'BNB']


def createTimeStamp():
    return int(time.time()*1000)


def param2string(param):
    """本函数用于根据param（一个参数字典）生成后缀字符串"""
    s = ''
    for k in param.keys():
        s += k
        s += '='
        s += str(param[k])
        s += '&'
    return s[:-1]


def hashing(query_string):
    """本函数用于根据后缀生成签名"""
    # 代码参考来源：https://github.com/binance-exchange/binance-signature-examples/blob/master/python/signature.py
    return hmac.new(apiSecretKey.encode('utf-8'), query_string.encode('utf-8'), hashlib.sha256).hexdigest()


def fetch_balance():
    data_timestamp = createTimeStamp()
    p = {'timestamp': data_timestamp}
    p['signature'] = hashing(param2string(p))
    # print(baseUrl+'/fapi/v1/time')
    response = requests.post(url=baseUrl+'/fapi/v2/balance',
                             headers={'X-MBX-APIKEY': apiKey}, data=p, proxies=proxies)
    print(response.status_code)


if __name__ == '__main__':
    fetch_balance()
