from celery import shared_task
from services.celery.tasks.notification import delete_notifications, expire_notifications


@shared_task
def update_notification_task():
    expire_notifications()


@shared_task
def delete_notifications_task():
    delete_notifications()
