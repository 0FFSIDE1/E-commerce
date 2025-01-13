from django.apps import AppConfig


class ProductsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'products'

    # def ready(self):
    #     from services.signals.product.vendor_total_product import update_total_products_on_create, update_total_products_on_delete
