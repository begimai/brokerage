from datetime import datetime

passed_params = ["--symbol=", "--currency=", "--start-date=", "--end-date="]
_stock_market_format = "%Y-%m-%d"
_symbol_max_length = 100
_currency_code_length = 3


def validate_date(date_text: str, desired_format: str = _stock_market_format) -> datetime.date:
    try:
        return datetime.strptime(date_text, desired_format).date()
    except ValueError:
        raise ValueError("Incorrect data format, should be YYYY-MM-DD.")
    except Exception as ex:
        raise ValueError("Incorrect desired data format.", ex.args[0])


def validate_and_get_end_date(date_text: str) -> datetime.date:
    if len(date_text) <= len(passed_params[3]):
        raise ValueError("Provide a value for the end-date parameter.")
    return validate_date(date_text[len(passed_params[3]):])


def validate_and_get_start_date(date_text: str) -> datetime.date:
    if len(date_text) <= len(passed_params[2]):
        raise ValueError("Provide a value for the start-date parameter.")
    return validate_date(date_text[len(passed_params[2]):])


def validate_and_get_currency(currency_text: str) -> str:
    if len(currency_text) != len(passed_params[1]) + _currency_code_length:
        raise ValueError("Currency should contain 3 characters.")
    return currency_text[len(passed_params[1]):]


def validate_and_get_symbol(symbol_text: str) -> str:
    if len(symbol_text) <= len(passed_params[0]):
        raise ValueError("Provide a value for the symbol parameter.")
    if len(symbol_text) > len(passed_params[0]) + _symbol_max_length:
        raise ValueError("Symbol's length cannot be more than 100 characters.")
    return symbol_text[len(passed_params[0]):]
