# Use the official Python image from the Docker Hub
FROM python:3.11-slim

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Set the working directory
WORKDIR /app

# Install dependencies
COPY requirements.txt /app/
RUN pip install --no-cache-dir -r requirements.txt

# Copy the entire Django project to the container
COPY . /app/

# Expose the port the app runs on
EXPOSE 8000
RUN python3 
# Run the Django development server
CMD ["gunicorn", "--bind", "0.0.0.0:8000", "myproject.wsgi:application"]

