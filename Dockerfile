FROM python:3.10-slim

# Install required system packages for mysqlclient
RUN apt-get update && apt-get install -y \
    default-libmysqlclient-dev \
    gcc \
    pkg-config \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Set working directory
WORKDIR /app

# Copy Python requirements
COPY requirements.txt .

# Upgrade pip & install Python packages
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

# Copy application code
COPY app/ app/

# Run Flask app
CMD ["python", "app/routes.py"]

