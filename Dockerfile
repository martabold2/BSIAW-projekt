# Use the official Python 3.8 image
FROM python:3.8-slim
# Set the working directory to /app
RUN apt-get update && apt-get install -y \
    unixodbc \
    unixodbc-dev \
    libodbc1 \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app
# Copy the current directory contents into the container at /app
COPY . /app
# Install the dependencies specified in requirements.txt
RUN pip install -r requirements.txt
# Expose port 3000 for the Flask app
EXPOSE 3000
# Command to run the Flask application
CMD python ./app.py