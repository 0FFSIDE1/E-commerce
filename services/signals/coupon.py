from django.db.models.signals import post_save
from django.dispatch import receiver
from coupons.models import Coupon
import random

@receiver(post_save, sender=Coupon)
def generate_coupon_code(sender, instance, created, **kwargs):
    """
    Signal to generate code for a newly created Coupon.

    Args:
        sender: The Coupon model.
        instance: The Coupon instance being saved.
        created: A boolean; True if a new Coupon instance is created.
        kwargs: Additional arguments passed by the signal.
    """
    if created:
        no = 'CDK12BXOEFLMNG4567HUVWYIQRS38JP90AT'
        no_list = [random.choice(no) for n in range(0,4)]
        code = ''.join(no_list) 
        Coupon.objects.filter(pk=instance.pk).update(code=f"CLXNG-{code}")
        



