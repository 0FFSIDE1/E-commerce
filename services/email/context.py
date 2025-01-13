
from datetime import timedelta
from django.utils import timezone
from app.models import AccountManager
from datetime import datetime

def context(order):
    order.save()
    items = [
        {
            'product_name': item.name,
            'size': item.size,
            'color': item.color,
            'quantity': item.quantity,
            'price': item.price,
            'total': item.total_price,
        }
        for item in order.orderitems.all()
    ]
    

    # Assuming created_at is timezone-aware
    issue_date = timezone.localtime(order.created_at) + timedelta(hours=1)
    due_date = timezone.localtime(order.created_at) + timedelta(hours=2)
    eta = timezone.localtime(due_date) + timedelta(days=5)
    account = AccountManager.objects.all().first()
    current_datetime = datetime.now().strftime('%Y-%m-%d %H:%M:%S') + timedelta(hours=1)
    

    data = {
                    'invoice_number': order.order_id,
                    'issue_date': issue_date,
                    'due_date': due_date,
                    'total_due': order.cart.total_amount,
                    'customer_name': order.customer.first_name + ' ' + order.customer.last_name,
                    'customer_email': order.customer.email,
                    'customer_phone': str(order.customer.phone),
                    'customer_address': order.customer.address + ', ' + order.customer.city + ', ' + order.customer.country,
                    'invoice_items': items,
                    'bank_name': account.bank_name,
                    'account_name': account.account_name,
                    'account_no': account.account_number,
                    'subtotal': order.total_amount,
                    'shipped_to': order.customer.address + ', ' + order.customer.city + ', ' + order.customer.country,
                    'payment_method': "Direct Bank Transfer",
                    'estimated_delivery_date': eta,
                    'order_number': order.order_id,
                    'order_items': items,
                    'transaction_date': current_datetime,
                }
    
    return data

def otp_context(otp_code):

    data = {
        'otp_code': otp_code,
    }

    return data


