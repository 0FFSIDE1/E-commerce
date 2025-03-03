from django.apps import AppConfig


class CouponsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'coupons'


    def ready(self):
        from services.signals.coupon import generate_coupon_code
