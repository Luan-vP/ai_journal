# Use the official Python image as the base image
FROM python:3.11-slim

RUN apt-get update && apt-get install -y \
    build-essential \
    libpq-dev \
    gcc \
    g++

# Set the working directory in the container
WORKDIR /app

# Copy the app source code to the container
COPY . .

# Install Poetry
RUN pip install poetry

# Use Poetry to install the Python dependencies
RUN poetry install

# Expose port 8000
EXPOSE 8000

# Start the FastAPI app
CMD ["poetry", "run", "uvicorn", "ai_journal.server:app", "--host", "0.0.0.0", "--port", "8000"]