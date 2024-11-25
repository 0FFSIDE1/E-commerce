from django.apps import AppConfig


class OrdersConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'orders'

    def ready(self):
        import services.signals.payment.initialize_payment
        from services.signals.sellers.total_order import update_vendor_total_orders, update_delivered_orders_for_vendor
