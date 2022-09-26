# Brokerage
This tool helps to get closing prices of a specific stock. Prices can be represented in other currencies as well.
SQLAlchemy is used as a database.
Stock prices are fetched form https://marketstack.com/ and currency values are from https://exchangeratesapi.io/.
Python 3.10.7 was used during the development.


## Obtain Access keys
Get access keys from https://marketstack.com/ and https://exchangeratesapi.io/ and store in environmental variables MARKET_STOCK_ACCESS_KEY and CURRENCY_ACCESS_KEY respectively.


# Run locally

## Install dependencies
Run following command in the root brokerage-tech-coding-challenge-master folder
```
pip install -r requirements.txt
```

## Run with desired parameters
```
python load_data.py --symbol=SPY --currency=USD --start-date=2022-02-02 --end-date=2022-03-03
```


## Future iterations
- add PEP8 and Linters,
- containerize.
