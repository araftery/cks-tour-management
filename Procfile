web: gunicorn wsgi:application
worker: celery --app=quadgrill worker --loglevel=info --concurrency=1