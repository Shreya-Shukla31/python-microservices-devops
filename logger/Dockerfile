#logger dockerfile code 
FROM python:3.11-slim

WORKDIR /app

# Install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY . .

ENV PYTHONUNBUFFERED=1

EXPOSE 6000
# Run app with Gunicorn
CMD ["gunicorn", "-b", "0.0.0.0:6000", "app:app"]