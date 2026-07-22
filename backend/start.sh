#!/bin/sh

# Set environment variables
export PYTHONUNBUFFERED=1
export HOST=0.0.0.0
export DEBUG=False

# Activate virtual environment (just in case)
echo 'Activating venv...'
python -m venv venv
source venv/bin/activate

# Install dependencies
echo 'Installing dependencies...'
pip install --no-cache-dir -r requirements.txt

# Run the application with gunicorn
exec gunicorn main:app --workers 2 --worker-class uvicorn.workers.UvicornWorker --bind 0.0.0.0:$PORT --access-logfile - --timeout 120