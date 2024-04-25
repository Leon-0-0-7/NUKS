from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base

engine = create_engine("sqlite:///tododatabase.db") #dodamo ime naše podatkovne baze
Base = declarative_base() #postavi instanco baze

#naredimo tabelo
class ToDo(Base):
    __tablename__="todotable"
    id = Column(Integer, primary_key = True)
    task = Column(String(50))
    params = Column(String(50))


