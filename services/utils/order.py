

# from app.tasks import admin_send_email
# from services.emails.utils.context import order_context

# def send_order_mail(status, order):
#     context = order_context(order)
#     if status == 'Paid':
#         admin_send_email.delay(context=context, email=order.customer.email, subject=f'Payment Successful: #{order.order_id}', body='emails/payment_success.html')
#     if status == 'Shipped':
#         admin_send_email.delay(context=context, email=order.customer.email, subject=f'Order Shipped: #{order.order_id}', body='emails/order_shipped.html')
#     if status == 'Delivered':
#         admin_send_email.delay(context=context, email=order.customer.email, subject=f'Order Delivered: #{order.order_id}', body='emails/order_delivered.html')
#     if status == 'Cancelled':
#         admin_send_email.delay(context=context, email=order.customer.email, subject=f'Order Cancelled: #{order.order_id}', body='emails/order_cancellled.html')
#     if status == 'Pending':
#         admin_send_email.delay(context=context, email=order.customer.email, subject=f'Order Pending: #{order.order_id}', body='emails/order_pending.html')
    
