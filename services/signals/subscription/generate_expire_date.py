from datetime import timedelta
from django.utils import timezone
from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver
from app.models import Subscription


@receiver(post_save, sender=Subscription)
def generate_end_date(sender, instance, created, **kwargs):
    if created:
        old_subscriptions = Subscription.objects.filter(user=instance.user, is_active=True)
        for sub in old_subscriptions:
            sub.is_active = False
            sub.save()
        instance.expire_date = instance.start_date + timedelta(days=instance.plan.duration_in_days)
        instance.save()
    
    else:
        instance.start_date = timezone.now()
        instance.expire_date = instance.start_date + timedelta(days=instance.plan.duration_in_days)
        current_sub = Subscription.objects.filter(user=instance.user, is_active=True).update(start_date=instance.start_date, expire_date=instance.expire_date)
        
    



        