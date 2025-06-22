# Use Python 3.13 slim image
FROM python:3.13-slim

# Set working directory
WORKDIR /app

# Set environment variables
ENV PYTHONPATH=/app
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Install system dependencies
RUN apt-get update && apt-get install -y \
    gcc \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements first for better caching
COPY store_analytics/requirements.txt ./store_analytics/requirements.txt
COPY requirements.txt ./

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt
RUN pip install --no-cache-dir -r store_analytics/requirements.txt

# Copy shared directory (needed for database models)
COPY shared/ ./shared/

# Copy store_analytics application
COPY store_analytics/ ./store_analytics/

# Create logs directory
RUN mkdir -p store_analytics/logs

# Expose port
EXPOSE 8001

# Command to run the application
CMD ["python", "-m", "uvicorn", "store_analytics.app.main:app", "--host", "0.0.0.0", "--port", "8001"]
