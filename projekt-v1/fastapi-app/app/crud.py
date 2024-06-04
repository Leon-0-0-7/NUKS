# fastapi-app/crud.py
from sqlalchemy.orm import Session
from . import models, schemas

def get_receipts(db: Session, skip: int = 0, limit: int = 10):
    return db.query(models.Receipt).offset(skip).limit(limit).all()

def create_receipt(db: Session, receipt: schemas.ReceiptCreate):
    db_receipt = models.Receipt(**receipt.dict())
    db.add(db_receipt)
    db.commit()
    db.refresh(db_receipt)
    return db_receipt