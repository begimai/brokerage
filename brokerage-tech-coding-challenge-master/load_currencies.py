import logging
import os

import requests

from model import create_instance, Currency

logging.getLogger().setLevel(logging.INFO)
_access_key = os.environ.get('CURRENCY_ACCESS_KEY')
_base_url = "http://api.marketstack.com/v1/"
_success_code = 200

if __name__ == '__main__':
    response = requests.get(f'{_base_url}currencies', params={"access_key": _access_key})
    if response.status_code != _success_code:
        logging.error("Something went wrong during the currency fetching")
        raise Exception("Something went wrong during the currency fetching")

    fetched_data = response.json()["data"]
    for currency in fetched_data:
        create_instance(Currency, code=currency["code"], name=currency["name"])
    logging.info("Successfully finished fetching currencies")
