from fastapi import FastAPI, Request, File, UploadFile, HTTPException
from fastapi.responses import HTMLResponse, FileResponse, Response
from database import SessionLocal, PDF


app = FastAPI()

async def list_uploaded_pdfs():
    db = SessionLocal()
    try:
        pdf_files = [pdf.filename for pdf in db.query(PDF).all()]
        return pdf_files
    finally:
        db.close()

@app.get("/")
async def read_root():
    pdf_files = await list_uploaded_pdfs()
    html_content = """
    <html>
    <head>
        <title>PDF Upload</title>
    </head>
    <body>
        <h1>Upload a PDF File</h1>
        <form id="uploadForm" enctype="multipart/form-data">
            <input type="file" name="file" accept=".pdf">
            <button type="button" onclick="uploadFile()">Upload</button>
        </form>
        <h1>Delete or Display Uploaded PDF</h1>
        <ul id="fileList">
    """
    for pdf_file in pdf_files:
        html_content += f"""
        <li>{pdf_file} 
            <button onclick='deleteFile("{pdf_file}")'>Delete</button>
            <button onclick='displayFile("{pdf_file}")'>Display</button>
        </li>
        """
    html_content += """
        </ul>
        <script>
            async function uploadFile() {
                const formData = new FormData();
                formData.append('file', document.querySelector('input[type="file"]').files[0]);
                try {
                    const response = await fetch('/upload', {
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

            async function deleteFile(filename) {
                try {
                    const response = await fetch(`/remove/${filename}`, {
                        method: 'DELETE'
                    });
                    if (response.ok) {
                        alert(`File ${filename} deleted successfully`);
                        location.reload(); // Refresh the page to update the file list
                    } else {
                        throw new Error('Failed to delete file');
                    }
                } catch (error) {
                    console.error(error);
                    alert('An error occurred while deleting the file');
                }
            }

            function displayFile(filename) {
                window.open(`/display/${filename}`);
            }
        </script>
    </body>
    </html>
    """
    return HTMLResponse(content=html_content, status_code=200)

# Doda pdf
#@app.post("/upload")
#async def upload_pdf(file: UploadFile = File(...)):
#    # Read PDF content from the uploaded file
#    pdf_content = await file.read()
#    # Save the uploaded file
#    with open(file.filename, "wb") as f:
#        f.write(pdf_content)
#    return {"message": "PDF uploaded successfully"}
@app.post("/upload")
async def upload_pdf(file: UploadFile = File(...)):
    db = SessionLocal()
    try:
        # Read PDF content from the uploaded file
        pdf_content = await file.read()
        # Save the uploaded file to the database
        db_pdf = PDF(filename=file.filename, content=pdf_content)
        db.add(db_pdf)
        db.commit()
        return {"message": "PDF uploaded successfully"}
    finally:
        db.close()

# Odstrani pdf
#@app.delete("/remove/{filename}")
#async def remove_pdf(filename: str):
#    try:
#        os.remove(filename)
#        return {"message": f"File {filename} removed successfully"}
#    except FileNotFoundError:
#        raise HTTPException(status_code=404, detail="File not found")
@app.delete("/remove/{filename}")
async def remove_pdf(filename: str):
    db = SessionLocal()
    try:
        db_pdf = db.query(PDF).filter(PDF.filename == filename).first()
        if db_pdf:
            db.delete(db_pdf)
            db.commit()
            return {"message": f"File {filename} removed successfully"}
        else:
            raise HTTPException(status_code=404, detail="File not found")
    finally:
        db.close()

# Prikaže v oknu
#@app.get("/display/{filename}")
#async def display_pdf(filename: str):
#    return FileResponse(filename)
@app.get("/display/{filename}")
async def display_pdf(filename: str):
    db = SessionLocal()
    try:
        db_pdf = db.query(PDF).filter(PDF.filename == filename).first()
        if db_pdf:
            return Response(content=db_pdf.content, media_type="application/pdf")
        else:
            raise HTTPException(status_code=404, detail="File not found")
    finally:
        db.close()

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="212.101.137.103", port=6000)