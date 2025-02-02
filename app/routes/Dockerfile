# Use an official Python base image
FROM python:3.9

# Set the working directory in the container
WORKDIR /app/routes

# Copy project files into the container
COPY . .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Expose port 8000 for FastAPI
EXPOSE 8000

# Run FastAPI app using Uvicorn
CMD ["uvicorn", "services:app", "--host", "0.0.0.0", "--port", "8000"]
