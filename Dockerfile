# Use official Python 3.12.4 slim image as base for smaller size
FROM python:3.12.4-slim

# Set working directory inside the container
WORKDIR /app

# Set environment variables
# - PYTHONUNBUFFERED: Ensures logs are printed in real-time
# - PYTHONDONTWRITEBYTECODE: Prevents .pyc files from being written
ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1

# Install system dependencies (e.g., for building packages if needed)
RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements file first (optimization: leverages Docker cache)
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the entire project into the container
COPY . .

# Expose port 8000 (default for FastAPI/Uvicorn)
EXPOSE 8000

# Run the FastAPI app with Uvicorn
# - host 0.0.0.0: Makes it accessible externally
# - port 8000: Matches exposed port
# - reload: Enables hot reloading (optional, remove for production)
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]