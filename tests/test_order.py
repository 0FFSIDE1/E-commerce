# filepath: /c:/Users/USER/cheexomglobal/orders/tests.py
from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User
from unittest.mock import MagicMock, patch
from customers.models import Customer
from orders.views import CreateOrderView, Order, Cart

class CreateOrderViewTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.url = reverse('create-customer')  # Ensure this matches your URL pattern name
        self.get_customer_url = reverse('customer')
        self.user_data = {
            "first_name": "John",
            "last_name": "Doe",
            "email": "john.doe@example.com",
            "phone": "+1234567890",
            "address": "123 Main St",
            "city": "Anytown",
            "country": "USA",
           
        }
        self.cart = Cart.objects.create()
        self.order_url = reverse('create-order')

   
   
    def test_create_order_invalid_method(self):
        response = self.client.get(self.order_url)
        self.assertEqual(response.status_code, 405)
        self.assertEqual(response.json()['success'], False)
        self.assertEqual(response.json()['message'], 'Invalid request method')

    def test_create_order_no_customer(self):
        
        response = self.client.post(self.order_url)
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json()['success'], False)
        self.assertIn('message', response.json())