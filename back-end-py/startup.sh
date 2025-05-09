#!/bin/bash

# Set the Python path to include the application directory
export PYTHONPATH=/home/site/wwwroot:$PYTHONPATH

# Install dependencies from requirements.txt
if [ -f /home/site/wwwroot/requirements.txt ]; then
    echo "Installing dependencies..."
    pip install -r /home/site/wwwroot/requirements.txt
fi

# Start the web application using Gunicorn
gunicorn --chdir /home/site/wwwroot --bind=0.0.0.0:8000 main:app