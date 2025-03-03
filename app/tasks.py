from datetime import date
from celery import shared_task
from app.models import Subscription
from services.celery.services.admin_send_email import admin_send_mail



@shared_task(bind=True)
def admin_send_email(self, to_email, subject, context, body):
    try:
    
        admin_send_mail(to_email, subject, context, body)
    except Exception as exc:
        self.retry(exc=exc, countdown=60)



@shared_task(bind=True)
def deactivate_expired_subscriptions(self):

    try:
        today = date.today()
        expired_subscriptions = Subscription.objects.filter(expire_date=today, is_active=True)
        for subscription in expired_subscriptions:
            subscription.deactivate()
            print(f"Deactivated subscription {subscription.id}")
    
    except Exception as exc:
        self.retry(exc=exc, countdown=60)
