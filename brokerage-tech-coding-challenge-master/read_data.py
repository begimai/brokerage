import logging

from extensions import session
from model import Stock

logging.getLogger().setLevel(logging.INFO)

# This is a sample how to read from the database.

if __name__ == '__main__':
    rows = session.query(Stock).all()
    logging.info(f'We have {len(rows)} rows in Stock table')
