# для створення таблиць у базі даних, тому всі поля мають бути описані саме для ств.таблиці

from sqlalchemy import Column, Integer, String, Date, func
from sqlalchemy.sql.sqltypes import DateTime
from sqlalchemy.ext.declarative import declarative_base


Base = declarative_base()


class Contact(Base):
    __tablename__ = "contacts"
    
    id = Column(Integer, primary_key=True, index=True)
    first_name = Column(String, index=True)
    last_name = Column(String, index=True)
    email = Column(String, unique=True, index=True)
    phone = Column(String)
    birthday = Column(Date)
    additional_info = Column(String, nullable=True)
    created_at = Column('created_at', DateTime, default=func.now())

