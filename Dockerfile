FROM python:3.11-slim

WORKDIR /app

# Install runtime dependencies (no gcc needed - wheels are precompiled)
RUN apt-get update && apt-get install -y --no-install-recommends \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements and install Python deps
COPY backend/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY backend/ .

# Create directory for SQLite database
RUN mkdir -p /app/data

# Set environment defaults (PORT is overridden by Railway)
ENV PYTHONUNBUFFERED=1 \
    HOST=0.0.0.0 \
    DEBUG=False

# Expose port (Railway will set actual PORT via env var)
EXPOSE 8787

# Run with gunicorn + uvicorn workers for production
# Railway replaces $PORT with the actual port number
CMD ["sh", "-c", "gunicorn main:app --workers 2 --worker-class uvicorn.workers.UvicornWorker --bind 0.0.0.0:$PORT --access-logfile - --timeout 120"]
