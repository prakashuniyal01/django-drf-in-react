# Use the official Python 3.12 image
FROM python:3.12-slim

# Install dependencies for psycopg2 and mysqlclient
RUN apt-get update && \
    apt-get install -y \
    libpq-dev \
    libmariadb-dev \
    pkg-config \
    gcc \
    && rm -rf /var/lib/apt/lists/*

# Set the working directory
WORKDIR /app

# Copy requirements.txt into the container
COPY requirements.txt /app/

# Install Python dependencies
RUN pip install --upgrade pip && \
    pip install -r requirements.txt

# Copy the rest of the application
COPY . /app/

# Expose port 8000 for Django
EXPOSE 8000

# Set the environment variable for Python
ENV PYTHONUNBUFFERED=1

# Run migrations and start the Django server
CMD ["bash", "-c", "python manage.py migrate && python manage.py runserver 0.0.0.0:8000"]
