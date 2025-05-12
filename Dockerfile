# Use an official Python runtime as a parent image
FROM python:3.10-slim

# Set environment variables for Python
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Set the working directory in the container
WORKDIR /usr/src/app

# Install system dependencies if any (e.g., for specific tools)
# RUN apt-get update && apt-get install -y --no-install-recommends some-package

# Install Poetry (optional, if you prefer Poetry for dependency management)
# RUN pip install poetry
# COPY poetry.lock pyproject.toml /usr/src/app/
# RUN poetry config virtualenvs.create false && poetry install --no-dev --no-interaction --no-ansi

# Install dependencies using requirements.txt
COPY requirements.txt /usr/src/app/
RUN pip install --no-cache-dir -r requirements.txt

# Copy the .env file
COPY .env /usr/src/app/

# Copy the rest of the application code into the container
COPY ./app /usr/src/app/app

# Expose the port the app runs on
EXPOSE 8000

# Command to run the application using Uvicorn
# The --reload flag is useful for development but should be removed for production
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]