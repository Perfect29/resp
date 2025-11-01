# Backend Dockerfile
FROM python:3.11-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    gcc \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements and install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY app/ ./app/
COPY .env* ./

# Expose port (Railway will set PORT, but we expose common ports)
EXPOSE 8000 8080

# Health check - Railway uses PORT environment variable
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD sh -c "curl -f http://localhost:${PORT:-8080}/health || exit 1"

# Run application - Railway sets PORT environment variable
# Use PORT if available, otherwise default to 8080 (Railway default)
# Remove --reload for production, use workers for better performance
CMD sh -c "exec uvicorn app.main:app --host 0.0.0.0 --port ${PORT:-8080} --workers 1"

