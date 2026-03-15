# Use explicit architecture for stability
FROM --platform=linux/amd64 python:3.11-slim

# Set working directory
WORKDIR /app

# Copy and install requirements
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY . .

# Expose the port
EXPOSE 5000

# Run with Gunicorn for professional performance
CMD ["gunicorn", "--bind", "0.0.0.0:5000", "app:app"]