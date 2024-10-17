# Use official Python image from DockerHub
FROM python:3.9-slim

# Set the working directory
WORKDIR /app

# Copy the requirements.txt file
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the entire app
COPY . .

# Set the environment variables for deployment
ENV SERVER_URL="0.0.0.0"
ENV PORT=10000

# Expose the port the app runs on
EXPOSE 10000

# Command to run the FastAPI app
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "10000"]