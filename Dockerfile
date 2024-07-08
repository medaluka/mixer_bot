# Use a lightweight Python base image
FROM python:3.12-slim

# Set the working directory
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Copy the requirements file into the container
COPY requirements.txt .

# Install Python dependencies, including Flask
RUN pip install --no-cache-dir -r requirements.txt

# Copy the application code into the container
COPY . .

# Define the TOKEN as an ARG and make it mandatory
ARG TOKEN
ENV TOKEN=${TOKEN}

# Add an entrypoint script to check for the TOKEN
COPY entrypoint.sh /entrypoint.sh
RUN chmod +x /entrypoint.sh

# Set the entrypoint
ENTRYPOINT ["/entrypoint.sh"]

# Expose the port for Cloud Run
EXPOSE 8080

# Set the command to run the application
CMD ["python", "main.py"]
