import logging
import sys

import numpy as np

from api_helpers import get_currency, get_market_stocks
from extensions import session
from helpers import print_stocks
from model import Stock
from validations import *

logging.getLogger().setLevel(logging.INFO)

if __name__ == '__main__':
    # Checking if all mandatory params
    if len(sys.argv) <= len(passed_params):
        raise ValueError("There are 4 mandatory input parameters: --symbol, --currency, --start-date, --end-date.")
    symbol = validate_and_get_symbol(sys.argv[1])
    currency = validate_and_get_currency(sys.argv[2])
    start_date = validate_and_get_start_date(sys.argv[3])
    end_date = validate_and_get_end_date(sys.argv[4])
    day_range = np.busday_count(start_date, end_date)
    if end_date.weekday() < 5:
        day_range += 1
    if day_range < 0:
        raise ValueError("Start date can't earlier than end date.")

    # SQLAlchemy Query to filter function
    base_query = session.query(Stock).filter(Stock.symbol == symbol,
                                             Stock.date >= start_date, Stock.date <= end_date)
    stocks = []
    if base_query.filter(Stock.currency == currency).count() == day_range:
        stocks = base_query.filter(Stock.currency == currency).all()
    elif base_query.group_by(Stock.symbol, Stock.date).count() != day_range:
        stocks = get_market_stocks(symbol, start_date, end_date)
    else:
        for grouped_stock in base_query.group_by(Stock.date, Stock.symbol):
            stock = base_query.filter(Stock.date == grouped_stock.date, Stock.symbol == grouped_stock.symbol)
            if stock.filter(Stock.currency == currency).first():
                stocks.append(base_query.filter(Stock.currency == currency).first())
            else:
                stocks.append(stock.first())
    for ind, stock in enumerate(stocks):
        if stock.currency != currency:
            stocks[ind] = get_currency(stock.currency, currency, stock.close_price, stock.date, stock.symbol)

    print_stocks(stocks)
