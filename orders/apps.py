from django.apps import AppConfig


class OrdersConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'orders'


    def ready(self):
        from services.signals.order.order import create_orderitems
        from services.signals.order.total_order import update_delivered_orders_for_vendor, update_vendor_total_orders_and_customers
