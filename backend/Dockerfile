FROM python:3.11-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && \
    apt-get install -y --no-install-recommends gcc g++ libpq-dev curl && \
    rm -rf /var/lib/apt/lists/*

# Copy and install Python dependencies
COPY requirements.txt .
RUN pip install --upgrade pip && pip install -r requirements.txt

# Copy application code
COPY . .

# Create startup script
RUN echo '#!/bin/bash\n\
set -e\n\
echo "Starting SMARTNEED backend..."\n\
echo "PORT: $PORT"\n\
echo "Working directory: $(pwd)"\n\
echo "Python path: $(which python)"\n\
echo "Contents: $(ls -la)"\n\
exec uvicorn app.main:app --host 0.0.0.0 --port ${PORT:-8000} --log-level info\n\
' > /app/start.sh && chmod +x /app/start.sh

# Expose port
EXPOSE 8000

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=30s --retries=3 \
    CMD curl -f http://localhost:8000/health || exit 1

# Start the application
CMD ["/app/start.sh"]
