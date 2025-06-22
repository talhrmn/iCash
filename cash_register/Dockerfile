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
COPY cash_register/requirements.txt ./cash_register/requirements.txt
COPY requirements.txt ./

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt
RUN pip install --no-cache-dir -r cash_register/requirements.txt

# Copy shared directory (needed for database models)
COPY shared/ ./shared/

# Copy cash_register application
COPY cash_register/ ./cash_register/

# Copy alembic configuration
COPY alembic/ ./alembic/
COPY alembic.ini ./

# Create logs directory
RUN mkdir -p cash_register/logs

# Expose port
EXPOSE 8000

# Command to run the application
CMD ["python", "-m", "uvicorn", "cash_register.app.main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]
