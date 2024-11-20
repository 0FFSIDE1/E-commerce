import requests
from django.conf import settings

def initialize_payment(order):
    """
    Initialize a payment with Paystack.
    :param email: Customer's email.
    :param amount: Amount in kobo (e.g., 100 Naira = 10000 Kobo).
    :param callback_url: URL to redirect after payment.
    :return: Response from Paystack.
    """
    headers = {
        "Authorization": f"Bearer {settings.PAYSTACK_SECRET_KEY}",
        "Content-Type": "application/json",
    }
    data = {
        "email": order.customer.email,
        "amount": int(order.total_price * 100),  # Convert to kobo
        "reference": order.order_id,
    }
    url = "https://api.paystack.co/transaction/initialize"
    response = requests.post(
        url, json=data, headers=headers
    )
    return response.json()
