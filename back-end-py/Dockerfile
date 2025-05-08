# Use a lightweight Python image
FROM python:3.9-slim

# Set the working directory inside the container
WORKDIR /app

# Copy only the requirements file first to leverage Docker caching
COPY requirements.txt /app/

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the backend files to the container
COPY . /app

# Expose the port the app runs on
EXPOSE 8000

# Start the backend application using Gunicorn
CMD ["gunicorn", "--bind", "0.0.0.0:8000", "--timeout", "600", "app.main:app"]