import sqlalchemy
from sqlalchemy import create_engine,Column,Integer,String
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

print(sqlalchemy.__version__)

engine = create_engine('sqlite:////home/sandesh/Desktop/DMS_V2/database.sqlite')

Session = sessionmaker(bind=engine)
session = Session()

Base = declarative_base()

class user(Base):
    __tablename__='user'
    name=Column(String(50),primary_key=True)
    password=Column(String(50))



q1=session.query(user).filter(user.name=='sandesh').first()
print(q1.name)

