from fastapi import FastAPI, File, UploadFile, HTTPException, status, Request, Form
from fastapi.responses import HTMLResponse, Response
from sqlalchemy.orm import Session
from database import engine, Base, Bill
import os
import shutil

#upload/main.py
from fastapi import FastAPI, File, UploadFile
from fastapi.responses import FileResponse
import os
from random import randint
import uuid
 
IMAGEDIR = "images/"


Base.metadata.create_all(engine)

app = FastAPI()

async def list_uploaded_pdfs():
    session = Session(bind=engine, expire_on_commit=False)
    try:
        pdf_files = [bill.description for bill in session.query(Bill).all()]
        return pdf_files
    finally:
        session.close()

@app.get("/", response_class=HTMLResponse)
async def read_root(request: Request):
    pdf_files = await list_uploaded_pdfs()

    html_content = f"""
    <html>
        <head>
            <title>Bill Management System</title>
        </head>
        <body>
            <h1>Bill Management System</h1>
            <p>Upload, view, and delete bills</p>
            <ul>
                <li><a href="{request.url_for('read_random_file')}">View Bills</a></li>
                <li><a href="{request.url_for('delete_bill', id=1)}">Delete Bill</a></li>
            </ul>

            <h1>Upload a Bill</h1>
            <form id="uploadBill" method="post" enctype="multipart/form-data">
                <label for="description">Description:</label>
                <input type="text" id="description" name="description"><br><br>
                <label for="file">File:</label>
                <input type="file" id="file" name="file"><br><br>
                <button type="button" onclick="uploadFile()">Upload file</button>
            </form>
            <h1>View and Delete Bills</h1>
            <ul id="billList">
    """
    for pdf_file in pdf_files:
        html_content += f"""
        <li>{pdf_file} 
            <button onclick='displayFile("{pdf_file}")'>Display</button>
        </li>
        """
    # Add your code to populate the bill list here
    html_content += """
        </ul>
        <script>
            // Add your JavaScript code here

            async function uploadFile() {
                const formData = new FormData();
                formData.append('file', document.querySelector('input[type="file"]').files[0]);
                formData.append('description', description.value);

                try {
                    const response = await fetch('/upload-bill', {
                        method: 'POST',
                        body: formData,
                    });
                    if (response.ok) {
                        alert('File uploaded successfully');
                        location.reload(); // Refresh the page to update the file list
                    } else {
                        throw new Error('Failed to upload file');
                    }
                } catch (error) {
                    console.error(error);
                    alert('An error occurred while uploading the file');
                }
            }

            
            function displayFile(description) {
                window.open(`/show/${description}`);
            }
        </script>
    </body>
    </html>
    """
    return HTMLResponse(content=html_content, status_code=200)

# @app.get("/upload-bill", response_class=HTMLResponse)
# async def read_upload_bill():
#     html_content = f"""
#     <html>
#         <head>
#             <title>Upload Bill</title>
#         </head>
#         <body>
#             <h1>Upload a Bill</h1>
#                 <form action="/upload-bill" method="post" enctype="multipart/form-data">
#                     <label for="description">Description:</label>
#                     <input type="text" id="description" name="description"><br><br>
#                     <label for="file">File:</label>
#                     <input type="file" id="file" name="file"><br><br>
#                     <input type="submit" value="Submit">
#                 </form>
#         </body>
#     </html>
#     """
#     return HTMLResponse(content=html_content, status_code=200)

# @app.post("/upload-bill", status_code=status.HTTP_201_CREATED)
# def upload_bill(file: UploadFile = File(...)):
#     session = Session(bind=engine, expire_on_commit=False)
#     try:
#         # Create the images directory if it does not exist
#         if not os.path.exists("images"):
#             os.makedirs("images")

#         file_location = f"images/{file.filename}"
#         with open(file_location, "wb") as buffer:
#             shutil.copyfileobj(file.file, buffer)
        
#         bill = Bill(description=file.filename, image_path=file.content)
#         session.add(bill)
#         session.commit()
#         return {"description": file.filename, "image_path": file_location}
#     finally:
#         session.close()
#         file.file.close()


@app.post("/upload-bill")
async def create_upload_file(description: str = Form(...), file: UploadFile = File(...)):
    # session = Session(bind=engine, expire_on_commit=False)

    # file.filename = f"{description}.jpg"
    # contents = await file.read()
 
    # #save the file
    # with open(f"{IMAGEDIR}{file.filename}", "wb") as f:
    #     f.write(contents)

    session = Session(bind=engine, expire_on_commit=False)
    try:
        # Create the images directory if it does not exist
        # if not os.path.exists(IMAGEDIR):
        #     os.makedirs(IMAGEDIR)
        
        file.filename = f"{description}.jpg"
        contents = await file.read()
        
        file_location = f"{IMAGEDIR}{file.filename}"
    
        #save the file
        with open(file_location, "wb") as f:
            f.write(contents)

        
        bill = Bill(description=file.filename, image_path=file_location)
        session.add(bill)
        session.commit()
        return {"description": file.filename, "image_path": file_location}
    
    finally:
        session.close()
        file.file.close()
 
    return {"filename": file.filename}


@app.get("/show/")
async def read_random_file():
 
    # get random file from the image directory
    files = os.listdir(IMAGEDIR)
    random_index = randint(0, len(files) - 1)
 
    path = f"{IMAGEDIR}{files[random_index]}"
     
    return FileResponse(path)

@app.get("/show/{description}")
async def read_selected_file(description: str):
    # get files from the image directory
    files = os.listdir(IMAGEDIR)
    matching_files = [file for file in files if description in file]

    if matching_files:
        # Select a random file from the matching files
        random_index = randint(0, len(matching_files) - 1)
        path = f"{IMAGEDIR}{matching_files[random_index]}"
        return FileResponse(path)
    else:
        return {"message": "No files found with the given description"}


@app.get("/bills")
def get_bills():
    session = Session(bind=engine, expire_on_commit=False)
    bills = session.query(Bill).first()

    session.close()
    return bills

@app.delete("/delete-bill/{id}")
def delete_bill(id: int):
    session = Session(bind=engine, expire_on_commit=False)
    bill = session.query(Bill).get(id)
    if bill:
        os.remove(bill.image_path)
        session.delete(bill)
        session.commit()
        session.close()
        return "Bill deleted"
    else:
        session.close()
        raise HTTPException(status_code=404, detail="Bill not found")





@app.get("/bills/{description}", response_class=HTMLResponse)
async def read_bill(description: str):
    session = Session(bind=engine, expire_on_commit=False)
    bill = session.query(Bill).filter(Bill.description == description).first()
    if bill:
        html_content = f"""
        <html>
            <head>
                <title>Bill {description}</title>
            </head>
            <body>
                <h1>Bill {description}</h1>
                <p>Description: {bill.description}</p>
                <p>Image Path: {bill.image_path}</p>
            </body>
        </html>
        """
        session.close()
        return HTMLResponse(content=html_content, status_code=200)
    else:
        session.close()
        raise HTTPException(status_code=404, detail="Bill not found")