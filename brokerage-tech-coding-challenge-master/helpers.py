from typing import List

from model import Stock


def print_stocks(stocks: List[Stock]) -> None:
    print('Requested stock information:')
    print('-' * 44)
    print('| date'.ljust(13), end='')
    print('| symbol'.ljust(9), end='')
    print('| currency'.ljust(11), end='')
    print('| price'.ljust(10), end='|\n')
    print('-' * 44)
    for stock in stocks:
        print(f'| {stock.date}'.ljust(13), end='')
        print(f'| {stock.symbol}'.ljust(9), end='')
        print(f'| {stock.currency}'.ljust(11), end='')
        print(f'| {stock.close_price}'.ljust(10), end='|\n')
    print('-' * 44)
