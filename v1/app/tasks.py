from celery import shared_task
from v1.services.celery.tasks.admin_send_email import admin_send_mail



@shared_task(bind=True)
def admin_send_email(self, to_email, subject, context, body):
    try:
    
        admin_send_mail(to_email, subject, context, body)
    except Exception as exc:
        self.retry(exc=exc, countdown=60)


