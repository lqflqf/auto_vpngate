from sqlalchemy import *
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class Mail(Base):
    __tablename__ = 'Mail'
    mail = Column(String(), primary_key=True)
    is_active = Column(Boolean())


class Country(Base):
    __tablename__ = 'Country'
    code_2 = Column(String(2), primary_key=True)
    code_3 = Column(String(3))
    country_name = Column(String())
    is_active = Column(Boolean())


class Parameter(Base):
    __tablename__ = 'Parameter'
    param_id = Column(String(8), primary_key=True)
    param_value = Column(JSON())
