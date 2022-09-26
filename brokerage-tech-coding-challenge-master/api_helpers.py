import logging
import os
from datetime import datetime

import requests
from requests import Response
from typing import List, Dict

from model import create_instance, Stock
from validations import validate_date

_market_stock_access_key = os.environ.get('MARKET_STOCK_ACCESS_KEY')
_exchange_rate_header = {
    "apikey": os.environ.get('CURRENCY_ACCESS_KEY')
}
_market_stock_url = "http://api.marketstack.com/v1/eod"
_exchange_rate_url = "https://api.apilayer.com/exchangerates_data/convert"
logging.getLogger().setLevel(logging.INFO)


def _validate_response(response: Response) -> Dict:
    if response.status_code != 200:
        raise Exception("Internal error, API request failed.", response.content)
    return response.json()


def get_market_stocks(symbol: str, start_date: datetime.date, end_date: datetime.date) -> List[Stock]:
    response = requests.get(_market_stock_url, params={"access_key": _market_stock_access_key, "symbols": symbol,
                                                       "date_from": start_date, "date_to": end_date})
    response = _validate_response(response)
    stocks = []
    for stock in reversed(response['data']):
        stocks.append(create_instance(Stock, date=validate_date(stock["date"][:10]),
                                      symbol=stock["symbol"], close_price=str(stock["close"])))
    return stocks


def get_currency(from_currency: str, to_currency: str, amount: int, date: datetime.date, symbol: str) -> Stock:
    response = requests.get(_exchange_rate_url, headers=_exchange_rate_header,
                            params={
                                "from": from_currency, "to": to_currency, "amount": amount, "date": date
                            })
    response = _validate_response(response)
    amount = round(float(response["result"]), 2)
    return create_instance(Stock, date=date, symbol=symbol, currency=to_currency, close_price=amount)
