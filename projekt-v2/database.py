from sqlalchemy import create_engine, Column, Integer, LargeBinary, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

Base = declarative_base()

class PDF(Base):
    __tablename__ = 'pdfs'

    id = Column(Integer, primary_key=True, autoincrement=True)
    filename = Column(String, unique=True)
    content = Column(LargeBinary)

engine = create_engine('sqlite:///pdfs.db')
Base.metadata.create_all(bind=engine)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# engine = create_engine("sqlite:///tododatabase.db") #dodamo ime naše podatkovne baze
# Base = declarative_base() #postavi instanco baze

# #naredimo tabelo
# class RACUN(Base):
#     __tablename__="racuni"
#     id = Column(Integer, primary_key = True)
#     imeslike = Column(String(50))
#     slika = Column(String(50))
