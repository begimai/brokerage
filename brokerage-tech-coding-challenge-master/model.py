import logging

from sqlalchemy import Column, CHAR, DATE, ForeignKey, Integer, String, UniqueConstraint
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.declarative import declarative_base

from extensions import session

Base = declarative_base()


class Currency(Base):
    __tablename__ = 'currencies'
    code = Column(CHAR(3), primary_key=True)
    name = Column(String(50))


class Stock(Base):
    __tablename__ = 'stocks'
    id = Column(Integer, primary_key=True)
    date = Column(DATE, nullable=False)
    symbol = Column(String(100), nullable=False)
    currency = Column(CHAR(3), ForeignKey('currencies.code'), nullable=False, default="USD")
    close_price = Column(String(8), nullable=False)
    __table_args__ = (UniqueConstraint('date', 'symbol', 'currency', name='date_symbol_currency'),)


def create_instance(model: Base, **params) -> Base:
    try:
        instance = model(**params)
        session.add(instance)
        session.commit()
        return instance
    except IntegrityError:
        # those errors happen on duplicate info, so just returning existing instance
        session.rollback()
        return session.query(model).filter_by(**params).first()
    except TypeError as e:
        # wrong format of data
        session.rollback()
        logging.error(e)
        raise ValueError(e)
    except Exception as e:
        logging.error(e)
