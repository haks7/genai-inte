# Use a base image with Python 3.10 or higher
FROM python:3.10-slim

# Set the working directory
WORKDIR /app

# Copy requirements file into the image
COPY requirements.txt .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application code into the image
COPY . .

# Expose the application port
EXPOSE 8000

# Use Gunicorn to serve the application
CMD ["gunicorn", "--bind", "0.0.0.0:8000", "--timeout", "600", "app.main:app"]