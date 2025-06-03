FROM python:3.12-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Copy the rest of the application
COPY . .

RUN ls -la

# Install the package
RUN pip install .

# Expose the port the app runs on
EXPOSE 80

# Command to run the application using FastAPI CLI
CMD ["fastapi", "run", "api.py", "--host", "0.0.0.0", "--port", "80"]