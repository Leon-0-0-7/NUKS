from sqlalchemy import create_engine, Column, Integer, String, Text, Date
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import declarative_base

engine = create_engine("sqlite:///bill_database.db")  # Adjust the database name accordingly
Base = declarative_base()  # Setup base class

class Bill(Base):
    __tablename__ = "billtable"
    id = Column(Integer, primary_key=True)
    description = Column(String(150))
    category = Column(String(150))
    image_path = Column(Text)  # Store the path to the image file
    purchase_date = Column(Date, index=True)
    entry_date = Column(Date, index=True)
