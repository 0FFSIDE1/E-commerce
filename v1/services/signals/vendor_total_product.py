from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from products.models import Product


@receiver(post_save, sender=Product)
def update_total_products_on_create(sender, instance, created, **kwargs):
    if created: # only update if a new product is created
        vendor = instance.vendor
        vendor.total_products = vendor.products.count()
        vendor.save()


@receiver(post_delete, sender=Product)
def update_total_products_on_delete(sender, instance, **kwargs):
    vendor = instance.vendor
    vendor.total_products = vendor.products.count()
    vendor.save()       
