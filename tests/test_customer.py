from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User
from customers.models import Customer
from django.db.utils import IntegrityError
import json

class CreateCustomerViewTest(TestCase):
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
            "create_account": True
        }

    
    def test_create_customer_success(self):
        response = self.client.post(self.url, json.dumps(self.user_data), content_type='application/json')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()['success'], True)
        self.assertEqual(response.json()['message'], 'Customer created successfully!')

    def test_create_user_duplicate_email(self):
        # Create a customer first
        self.client.post(self.url, json.dumps(self.user_data), content_type='application/json')
        # Try to create the same customer again
        response = self.client.post(self.url, json.dumps(self.user_data), content_type='application/json')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()['success'], True)
        self.assertEqual(response.json()['message'], 'Customer updated successfully!')

    def test_update_customer_success(self):
        self.client.post(self.url, json.dumps(self.user_data), content_type='application/json')
        change_phone = self.user_data.copy()
        change_phone['phone'] = '09054278392'
      
        response = self.client.post(self.url, json.dumps(change_phone), content_type='application/json')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()['success'], True)
        self.assertEqual(response.json()['message'], 'Customer updated successfully!')

    def test_invalid_request_method(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 405)
        self.assertEqual(response.json()['success'], False)
        self.assertEqual(response.json()['message'], 'Invalid request method')

    def test_create_customer_without_account(self):
        data_without_account = self.user_data.copy()
        data_without_account['create_account'] = False
        response = self.client.post(self.url, json.dumps(data_without_account), content_type='application/json')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()['success'], True)
        self.assertEqual(response.json()['message'], 'Customer created successfully!')


    def test_get_customer_view_authenticated(self):
        response = self.client.post(self.url, json.dumps(self.user_data), content_type='application/json')
        response = self.client.get(self.get_customer_url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()['success'], True)
        self.assertEqual(response.json()['customer']['email'], 'john.doe@example.com')

    def test_get_customer_view_unauthenticated(self):
        response = self.client.post(self.url, json.dumps(self.user_data), content_type='application/json')
        response = self.client.get(self.get_customer_url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()['success'], True)
        self.assertEqual(response.json()['message'], 'Customer details retrieved successfully')
