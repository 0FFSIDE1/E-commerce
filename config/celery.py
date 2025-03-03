from __future__ import absolute_import, unicode_literals
import os
from celery import Celery

# Set default Django settings module for Celery
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')

app = Celery('config')

app.conf.update(
    broker_url=os.environ.get('CELERY_BROKER_URL'),
    broker_connection_retry=True,  # Retry broker connections during runtime
    broker_connection_retry_on_startup=True,  # Retry broker connections during startup
    worker_pool='solo',  # Use the solo pool
)
app.conf.timezone = 'UTC'  # Matches Django TIME_ZONE
app.conf.enable_utc = True  # Always enable UTC
# Using a string here means the worker doesn’t have to serialize # the configuration object to child processes.
app.config_from_object('django.conf:settings', namespace='CELERY')

# Automatically discover tasks in registered Django apps
app.autodiscover_tasks()

@app.task(bind=True)
def debug_task(self):
    print(f'Request: Everything is fine!')
