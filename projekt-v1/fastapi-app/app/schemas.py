# fastapi-app/schemas.py
from pydantic import BaseModel
from datetime import date

class ReceiptBase(BaseModel):
    name: str
    category: str
    purchase_date: date
    entry_date: date

class ReceiptCreate(ReceiptBase):
    image_url: str

class Receipt(ReceiptBase):
    id: int

    class Config:
        orm_mode = True