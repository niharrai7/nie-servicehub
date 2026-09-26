# Use official lightweight Python base image
FROM python:3.11-slim

# Set environment variables to prevent bytecode files and enable unbuffered output
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

# Set working directory inside container
WORKDIR /app

# Copy dependency definition file
COPY requirements.txt .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy backend application source code
COPY app ./app

# Expose backend port
EXPOSE 8000

# Start Uvicorn ASGI server
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
