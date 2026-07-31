FROM python:3.10-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    gcc \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy bot code
COPY . .

# Create logs directory
RUN mkdir -p logs

# Health check
HEALTHCHECK --interval=60s --timeout=10s --start-period=40s --retries=3 \
    CMD python -c "import os; exit(0 if os.path.exists('bot.log') else 1)"

# Run bot with auto-restart
CMD ["python3", "run_24_7.py"]
