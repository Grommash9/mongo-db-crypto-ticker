from models import BinanceApi, WhiteBitApi, HuobiApi
import logging
import pymongo
from pymongo import UpdateOne
import config

logging.basicConfig(format='%(asctime)s - %(filename)s - %(funcName)s - %(levelname)s - %(message)s',
                    filename='ticker_getter.log', encoding='utf-8', level=logging.WARNING)


def get_binance_ticker_data():
    binance = BinanceApi()
    return binance.get_tickers()


def get_white_bit_ticker_data():
    white_bit_data_clear_list = []
    white_bit = WhiteBitApi()
    white_bit_ticker_data = white_bit.get_tickers()
    for ticker_name, ticker_data in white_bit_ticker_data.items():
        white_bit_data_clear_list.append({'symbol': ticker_name.replace("_", ''),
                                          'price': ticker_data['last_price']})
    return white_bit_data_clear_list


def get_huobi_ticker_data():
    huobi_tickers_data = []
    huobi_client = HuobiApi()
    huobi_tickers = huobi_client.get_tickers()

    for ticker_data in huobi_tickers['data']:
        huobi_tickers_data.append({'symbol': ticker_data['symbol'].upper(),
                                   'price': (float(ticker_data['bid']) + float(ticker_data['ask'])) / 2})
    return huobi_tickers_data


def save_ticker_data_to_db(ticker_list, exchange_title):
    operations_to_process = []
    conn = pymongo.MongoClient(f"mongodb+srv://{config.user}:{config.password}@cluster0.sljwohc.mongodb.net/", 27017)

    db = conn.crypto
    collection = db.tickers

    for ticker in ticker_list:
        operations_to_process.append(UpdateOne(
            {'symbol': ticker['symbol']},
            {'$set': {exchange_title: float(ticker['price'])}},
            upsert=True
        ))

    collection.bulk_write(operations_to_process)
    conn.close()


if __name__ == "__main__":

    wb_ticker_data = get_white_bit_ticker_data()
    binance_ticker_data = get_binance_ticker_data()
    huobi_ticker_data = get_huobi_ticker_data()

    for data_list, exchange_title in ((wb_ticker_data, 'white_bit'), (binance_ticker_data, 'binance'),
                                      (huobi_ticker_data, 'huobi')):
        save_ticker_data_to_db(data_list, exchange_title)
