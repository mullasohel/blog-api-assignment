# Use an official Python image
FROM python:3.11-slim

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Set working directory
WORKDIR /app

# Install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy project files
COPY . .

# Expose the port Gunicorn will run on
EXPOSE 8000

# Collect static files
RUN python manage.py collectstatic --noinput

# Start the server using Gunicorn
CMD ["gunicorn", "blog_project.wsgi:application", "--bind", "0.0.0.0:8000"]
