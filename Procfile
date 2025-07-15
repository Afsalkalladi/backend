web: gunicorn eesa_backend.wsgi --log-file -
release: python manage.py migrate --settings=eesa_backend.settings_production
