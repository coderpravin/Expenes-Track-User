FROM python:3.10-slim

# Install system dependencies required for pycairo, xhtml2pdf, and other libs
RUN apt-get update && apt-get install -y \
    libcairo2 \
    libcairo2-dev \
    pkg-config \
    libffi-dev \
    libgdk-pixbuf2.0-dev \
    gcc \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# Copy requirements first to leverage Docker cache
COPY requirements.txt /app/
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application
COPY . /app/

# Default command (can be overridden by Jenkins)
CMD ["python", "project/manage.py", "check"]
