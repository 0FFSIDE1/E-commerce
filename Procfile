web: python manage.py collectstatic --no-input && gunicorn config.wsgi:application --bind 0.0.0.0:$PORT --workers 3 --timeout 30 
release: python manage.py makemigrations && python manage.py migrate
