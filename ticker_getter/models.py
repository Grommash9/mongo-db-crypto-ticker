import requests


class BinanceApi:

    def __init__(self):
        self.__host = 'https://api.binance.com'

    def get_tickers(self):
        request = '/api/v3/ticker/price'
        response = requests.get(self.__host + request)
        return response.json()


class WhiteBitApi:

    def __init__(self):
        self.__host = 'https://whitebit.com'

    def get_tickers(self):
        request = '/api/v4/public/ticker'
        response = requests.get(self.__host + request)
        return response.json()


class HuobiApi:

    def __init__(self):
        self.__host = 'https://api.huobi.pro'

    def get_tickers(self):
        request = '/market/tickers'
        response = requests.get(self.__host + request)
        return response.json()


