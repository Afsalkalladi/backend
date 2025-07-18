# Docker Setup for EESA Backend

This document explains how to run the EESA Backend using Docker.

## Quick Start

### Option 1: Using Docker Compose (Recommended)

This will start both the Django app and PostgreSQL database:

```bash
# Build and start all services
docker-compose up --build

# Or run in background
docker-compose up --build -d

# View logs
docker-compose logs -f web

# Stop services
docker-compose down
```

The application will be available at: http://localhost:8000

### Option 2: Using Docker only

If you have your own database:

```bash
# Build the image
docker build -t eesa-backend .

# Run with environment variables
docker run -p 8000:8000 \
  -e DEBUG=False \
  -e DB_HOST=your-db-host \
  -e DB_NAME=your-db-name \
  -e DB_USER=your-db-user \
  -e DB_PASSWORD=your-db-password \
  -e SECRET_KEY=your-secret-key \
  -e ALLOWED_HOSTS=localhost,127.0.0.1 \
  eesa-backend
```

## What Happens During Container Startup

The Docker container automatically:

1. ✅ **Checks database connection**
2. ✅ **Generates any missing migrations**
3. ✅ **Runs database migrations**
4. ✅ **Creates superuser** (admin/admin123)
5. ✅ **Collects static files**
6. ✅ **Starts Gunicorn server**

## Admin Access

After container starts, you can access the admin panel:

- **URL**: http://localhost:8000/eesa/
- **Username**: admin
- **Password**: admin123

⚠️ **Important**: Change the default password after first login!

## Environment Variables

Required environment variables:

| Variable | Description | Example |
|----------|-------------|---------|
| `DB_HOST` | Database host | `db` or `localhost` |
| `DB_NAME` | Database name | `eesa_backend` |
| `DB_USER` | Database user | `postgres` |
| `DB_PASSWORD` | Database password | `postgres123` |
| `SECRET_KEY` | Django secret key | `your-secret-key` |
| `ALLOWED_HOSTS` | Allowed hosts | `localhost,127.0.0.1` |

Optional:
| Variable | Description | Default |
|----------|-------------|---------|
| `DEBUG` | Debug mode | `False` |
| `DB_PORT` | Database port | `5432` |

## Troubleshooting

### Database Connection Issues

```bash
# Check if database is running
docker-compose ps

# Check web service logs
docker-compose logs web

# Restart services
docker-compose restart
```

### Migration Issues

```bash
# Connect to container and run migrations manually
docker-compose exec web python manage.py migrate

# Check migration status
docker-compose exec web python manage.py showmigrations
```

### Reset Everything

```bash
# Stop and remove all containers and volumes
docker-compose down -v

# Rebuild and start fresh
docker-compose up --build
```

## Production Deployment

For production, make sure to:

1. Use strong `SECRET_KEY`
2. Set `DEBUG=False`
3. Configure proper `ALLOWED_HOSTS`
4. Use external PostgreSQL database
5. Set up proper environment variables
6. Use Docker secrets for sensitive data

## Support

If you encounter issues:

1. Check the logs: `docker-compose logs web`
2. Verify environment variables are set correctly
3. Ensure database is running and accessible
4. Check if ports are available (8000 for web, 5432 for db)
