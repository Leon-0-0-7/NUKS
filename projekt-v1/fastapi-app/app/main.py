from fastapi import FastAPI, File, UploadFile, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from app import models, schemas, crud
from app.database import SessionLocal, engine
from typing import List
import os

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

# Set up CORS
origins = [
    "http://212.101.137.103:5080",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.post("/upload")
async def upload_image(file: UploadFile = File(...)):
    file_location = os.path.join("/app/files", file.filename)
    with open(file_location, "wb+") as file_object:
        file_object.write(file.file.read())
    print(f"filename: files/{file.filename}, file_location: {file_location}, file_object: {file_object}")
    return {"filename": f"files/{file.filename}"}  # Return relative path for the URL

@app.post("/receipts/", response_model=schemas.Receipt)
def create_receipt(receipt: schemas.ReceiptCreate, db: Session = Depends(get_db)):
    return crud.create_receipt(db=db, receipt=receipt)

@app.get("/receipts/", response_model=List[schemas.Receipt])
def read_receipts(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    receipts = crud.get_receipts(db, skip=skip, limit=limit)
    return receipts

@app.delete("/receipts/")
def delete_all_receipts(db: Session = Depends(get_db)):
    receipts = db.query(models.Receipt).all()
    if not receipts:
        raise HTTPException(status_code=404, detail="No receipts found to delete.")
    
    for receipt in receipts:
        db.delete(receipt)
    
    db.commit()
    return {"detail": "All receipts deleted."}
