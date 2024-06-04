from fastapi import FastAPI, File, UploadFile, HTTPException, status, Request, Form
from fastapi.responses import HTMLResponse, FileResponse, JSONResponse
from sqlalchemy.orm import Session
from database import engine, Base, Bill
import os
import shutil
from fastapi.staticfiles import StaticFiles
from random import randint
from datetime import datetime


IMAGEDIR = "images/"

Base.metadata.create_all(engine)

app = FastAPI()

app.mount("/frontend", StaticFiles(directory="frontend"), name="frontend")


@app.get("/", response_class=HTMLResponse)
async def read_root(request: Request):
    with open("frontend/index.html", "r") as file:
        html_content = file.read()
    return HTMLResponse(content=html_content, status_code=200)


@app.get("/api/bills", response_class=JSONResponse)
async def get_bills():
    session = Session(bind=engine, expire_on_commit=False)
    try:
        bills = session.query(Bill).all()
        bills_list = [
            {
                "description": bill.description,
                "image_path": bill.image_path,
                "category": bill.category,
                "purchase_date": bill.purchase_date.isoformat() if bill.purchase_date else None,
                "entry_date": bill.entry_date.isoformat() if bill.entry_date else None
            } for bill in bills]
        return JSONResponse(content=bills_list)
    finally:
        session.close()

@app.post("/upload-bill")
async def create_upload_file(
    description: str = Form(...),
    category: str = Form(...),
    purchase_date: str = Form(...),
    entry_date: str = Form(...),
    file: UploadFile = File(...)
):
    session = Session(bind=engine, expire_on_commit=False)
    try:
        file.filename = f"{description}.jpg"
        contents = await file.read()
        file_location = f"{IMAGEDIR}{file.filename}"

        with open(file_location, "wb") as f:
            f.write(contents)

        purchase_date_parsed = datetime.strptime(purchase_date, "%Y-%m-%d").date()
        entry_date_parsed = datetime.strptime(entry_date, "%Y-%m-%d").date()

        bill = Bill(
            description=file.filename,
            image_path=file_location,
            category=category,
            purchase_date=purchase_date_parsed,
            entry_date=entry_date_parsed
        )
        session.add(bill)
        session.commit()
        return {
            "description": file.filename,
            "image_path": file_location,
            "category": category,
            "purchase_date": purchase_date,
            "entry_date": entry_date
        }
    finally:
        session.close()
        file.file.close()


@app.get("/show/")
async def read_random_file():
    files = os.listdir(IMAGEDIR)
    random_index = randint(0, len(files) - 1)
    path = f"{IMAGEDIR}{files[random_index]}"
    return FileResponse(path)


@app.get("/show/{description}")
async def read_selected_file(description: str):
    files = os.listdir(IMAGEDIR)
    matching_files = [file for file in files if description in file]
    if matching_files:
        random_index = randint(0, len(matching_files) - 1)
        path = f"{IMAGEDIR}{matching_files[random_index]}"
        return FileResponse(path)
    else:
        return {"message": "No files found with the given description"}

@app.delete("/delete-all")
async def delete_all_files():
    session = Session(bind=engine, expire_on_commit=False)
    try:
        session.query(Bill).delete()
        session.commit()
        for filename in os.listdir(IMAGEDIR):
            file_path = os.path.join(IMAGEDIR, filename)
            if os.path.isfile(file_path):
                os.remove(file_path)
        return {"message": "All receipts deleted successfully"}
    finally:
        session.close()
