import unittest
from datetime import date
from unittest.mock import MagicMock, patch

from api_helpers import get_currency, get_market_stocks
from extensions import session
from model import create_instance, Stock
from validations import *


class TestApiRequest(unittest.TestCase):
    @patch('requests.get')
    def test_get_currency(self, mock_requests):
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            'result': 55
        }
        mock_requests.return_value = mock_response
        returned_instance = get_currency("USD", "EUR", 100, datetime.now().date(), "Symbol")
        fetched_instance = session.query(Stock).filter(Stock.date == datetime.now().date(), Stock.symbol == "Symbol",
                                                       Stock.currency == "EUR").first()
        self.assertEqual(returned_instance.id, fetched_instance.id)
        self.assertEqual(returned_instance.date, fetched_instance.date)
        self.assertEqual(returned_instance.symbol, fetched_instance.symbol)
        self.assertEqual(returned_instance.currency, fetched_instance.currency)
        self.assertEqual(returned_instance.close_price, fetched_instance.close_price)

    @patch('requests.get')
    def test_get_currency_with_bad_request(self, mock_requests):
        mock_response = MagicMock()
        mock_response.status_code = 400
        mock_requests.return_value = mock_response
        with self.assertRaises(Exception) as e:
            get_currency("USD", "111", 100, datetime.now().date(), "Symbol")
        self.assertEqual("Internal error, API request failed.", e.exception.args[0])
        count = session.query(Stock).filter(Stock.date == datetime.now().date(), Stock.symbol == "Symbol",
                                            Stock.currency == "111").count()
        self.assertEqual(0, count)

    @patch('requests.get')
    def test_get_market_stocks(self, mock_requests):
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            'data': [
                {
                    "close": 151.0,
                    "symbol": "Sym",
                    "date": "2022-09-09T00:00:00+0000"
                },
                {
                    "close": 150.43,
                    "symbol": "Sym",
                    "date": str(datetime.now())
                }
            ]
        }
        mock_requests.return_value = mock_response
        returned_instances = get_market_stocks("Sym", datetime.now().date(), datetime.now().date())
        self.assertEqual(2, len(returned_instances))
        self.assertEqual("Sym", returned_instances[0].symbol)
        self.assertEqual("USD", returned_instances[0].currency)
        self.assertEqual("150.43", returned_instances[0].close_price)
        self.assertEqual(datetime.now().date(), returned_instances[0].date)
        self.assertEqual("Sym", returned_instances[1].symbol)
        self.assertEqual("USD", returned_instances[1].currency)
        self.assertEqual("151.0", returned_instances[1].close_price)
        self.assertEqual(datetime.strptime("2022-09-09", "%Y-%m-%d").date(), returned_instances[1].date)


class TestModel(unittest.TestCase):
    def test_create_instance(self):
        initial_count = session.query(Stock).count()
        new_instance = create_instance(Stock,
                                       date=datetime.now().date(), symbol="Symbol", currency="333", close_price=10)
        self.assertEqual(session.query(Stock).count(), initial_count + 1)
        fetched_instance = session.query(Stock).filter(Stock.date == datetime.now().date(), Stock.symbol == "Symbol",
                                                       Stock.currency == "333").first()
        self.assertEqual(new_instance.id, fetched_instance.id)
        self.assertEqual(new_instance.date, fetched_instance.date)
        self.assertEqual(new_instance.symbol, fetched_instance.symbol)
        self.assertEqual(new_instance.currency, fetched_instance.currency)
        self.assertEqual(new_instance.close_price, fetched_instance.close_price)

    def test_create_duplicate_instance_returns_old_instance(self):
        initial_count = session.query(Stock).count()
        first_instance = create_instance(Stock,
                                         date=datetime.now().date(), symbol="Symbol", currency="333", close_price=10)
        self.assertEqual(session.query(Stock).count(), initial_count + 1)
        second_instance = create_instance(Stock, date=first_instance.date, symbol=first_instance.symbol,
                                          currency=first_instance.currency, close_price=5654)
        self.assertEqual(session.query(Stock).count(), initial_count + 1)
        self.assertEqual(first_instance.id, second_instance.id)
        self.assertEqual(first_instance.date, second_instance.date)
        self.assertEqual(first_instance.symbol, second_instance.symbol)
        self.assertEqual(first_instance.currency, second_instance.currency)
        self.assertEqual(first_instance.close_price, second_instance.close_price)


class TestValidators(unittest.TestCase):
    def test_validate_date(self):
        validated_date = validate_date("2020-10-10")
        self.assertEqual(validated_date.day, 10)
        self.assertEqual(validated_date.month, 10)
        self.assertEqual(validated_date.year, 2020)
        self.assertTrue(isinstance(validated_date, date))

    def test_validate_date_with_wrong_date(self):
        with self.assertRaises(ValueError) as e:
            validate_date("2020-20-10")
        self.assertEqual("Incorrect data format, should be YYYY-MM-DD.", e.exception.args[0])

    def test_validate_date_with_date_format(self):
        validated_date = validate_date("2020-20-10", "%Y-%d-%m")
        self.assertEqual(validated_date.day, 20)
        self.assertEqual(validated_date.month, 10)
        self.assertEqual(validated_date.year, 2020)
        self.assertTrue(isinstance(validated_date, date))

    def test_validate_date_with_wrong_date_format(self):
        with self.assertRaises(ValueError) as e:
            validate_date("2020-20-10", "%Y-%Y-%Y")
        self.assertEqual("Incorrect desired data format.", e.exception.args[0])

    def test_validate_and_get_end_date(self):
        validated_date = validate_and_get_end_date("--end-date=2020-10-10")
        self.assertEqual(validated_date.day, 10)
        self.assertEqual(validated_date.month, 10)
        self.assertEqual(validated_date.year, 2020)
        self.assertTrue(isinstance(validated_date, date))

    def test_validate_and_get_end_date_with_no_date(self):
        with self.assertRaises(ValueError) as e:
            validate_and_get_end_date("--end-date=")
        self.assertEqual("Provide a value for the end-date parameter.", e.exception.args[0])

    def test_validate_and_get_start_date(self):
        validated_date = validate_and_get_start_date("--start-date=2020-10-10")
        self.assertEqual(validated_date.day, 10)
        self.assertEqual(validated_date.month, 10)
        self.assertEqual(validated_date.year, 2020)
        self.assertTrue(isinstance(validated_date, date))

    def test_validate_and_get_start_date_with_no_date(self):
        with self.assertRaises(ValueError) as e:
            validate_and_get_start_date("--start-date=")
        self.assertEqual("Provide a value for the start-date parameter.", e.exception.args[0])

    def test_validate_and_get_currency(self):
        validated_currency = validate_and_get_currency("--currency=HEY")
        self.assertEqual("HEY", validated_currency)

    def test_validate_and_get_currency_with_wrong_length(self):
        with self.assertRaises(ValueError) as e:
            validate_and_get_currency("--currency=HI")
        self.assertEqual("Currency should contain 3 characters.", e.exception.args[0])

    def test_validate_and_get_symbol(self):
        validated_currency = validate_and_get_symbol("--symbol=HELLO")
        self.assertEqual("HELLO", validated_currency)

    def test_validate_and_get_symbol_with_no_value(self):
        with self.assertRaises(ValueError) as e:
            validate_and_get_symbol("--symbol=")
        self.assertEqual("Provide a value for the symbol parameter.", e.exception.args[0])

    def test_validate_and_get_symbol_with_wrong_length(self):
        with self.assertRaises(ValueError) as e:
            validate_and_get_symbol("--symbol=" + "HELLO" * 21)
        self.assertEqual("Symbol's length cannot be more than 100 characters.", e.exception.args[0])


if __name__ == '__main__':
    unittest.main()
