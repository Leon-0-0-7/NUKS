# Use the official Python image as a base image
FROM python:3.11-slim

# Set the working directory inside the container
WORKDIR /app

# Copy the application files into the container
COPY main.py .
COPY database.py .
# COPY pdfs.db .
COPY requirements.txt .

# Install the Python dependencies
RUN pip install -r requirements.txt

# Expose port 8000 to the outside world
EXPOSE 6000

# Command to run the FastAPI application using Uvicorn
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "6000"]