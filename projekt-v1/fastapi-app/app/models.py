# fastapi-app/models.py
from sqlalchemy import Column, Integer, String, Date
from .database import Base

class Receipt(Base):
    __tablename__ = "receipts"

    id = Column(Integer, primary_key=True, index=True)
    image_url = Column(String, index=True)
    name = Column(String, index=True)
    category = Column(String, index=True)
    purchase_date = Column(Date)
    entry_date = Column(Date)