# Use an official Python runtime as the base image
FROM python:3.10.11

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Set the working directory in the container
WORKDIR /

# Install dependencies
COPY requirements.txt /
RUN python3 -m pip install -r requirements.txt

# Copy the rest of the application code to the working directory
COPY . /

# Expose port 8000
EXPOSE 8000

# Command to run the application using Gunicorn (or Django's built-in development server for development)
CMD ["gunicorn", "--bind", "0.0.0.0:8000", "Together.wsgi:application"]
