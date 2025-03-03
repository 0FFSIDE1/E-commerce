from django.db import models

# Create your models here.
class Coupon(models.Model):
  
    coupon_name = models.CharField(max_length=20, default=None, blank=False, null=False)
    discount = models.PositiveIntegerField(default=None)
    code = models.CharField(max_length=10, default=None, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return f"Coupon: {self.coupon_name} | {self.code}"

