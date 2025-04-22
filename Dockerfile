FROM python:3.13-slim

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV PYTHONPATH=/app

WORKDIR /app

# Install poetry
RUN pip install --no-cache-dir poetry

# Copy poetry configuration files
COPY pyproject.toml ./

# Configure poetry to not create a virtual environment
RUN poetry config virtualenvs.create false

# Install dependencies
RUN poetry install --only main --no-root

# Copy application code
COPY . .

# Expose the port the app runs on
EXPOSE 5000

# Command to run the application with gunicorn
CMD ["gunicorn", "--bind", "0.0.0.0:5000", "wsgi:app"]
