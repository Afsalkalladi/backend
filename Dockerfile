# Multi-stage build for optimized production image
FROM python:3.11-slim as builder

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Install system dependencies for building
RUN apt-get update \
    && apt-get install -y --no-install-recommends gcc libpq-dev \
    && rm -rf /var/lib/apt/lists/*

# Create virtual environment
RUN python -m venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH"

# Install Python dependencies
COPY requirements.txt /app/
WORKDIR /app
RUN pip install --upgrade pip && pip install -r requirements.txt

# Production stage
FROM python:3.11-slim as production

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Install runtime dependencies only
RUN apt-get update \
    && apt-get install -y --no-install-recommends libpq5 \
    && rm -rf /var/lib/apt/lists/*

# Create a non-root user
RUN groupadd -r django && useradd -r -g django django

# Copy virtual environment from builder stage
COPY --from=builder /opt/venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH"

# Set work directory
WORKDIR /app

# Copy project
COPY . /app/

# Change ownership to django user
RUN chown -R django:django /app

# Switch to django user
USER django

# Collect static files
RUN python manage.py collectstatic --noinput

# Expose port (will be overridden by Render)
EXPOSE 8000

# Create startup script
RUN echo '#!/bin/bash\npython manage.py migrate\nexec gunicorn eesa_backend.wsgi:application --bind 0.0.0.0:${PORT:-8000}' > /app/start.sh && chmod +x /app/start.sh

# Start Gunicorn server
CMD ["/app/start.sh"] 