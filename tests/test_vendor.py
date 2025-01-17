from django.test import TestCase, Client
from django.urls import reverse
from rest_framework import status
from django.contrib.auth.models import User
from carts.models import Cart, CartItem
from customers.models import Customer
from orders.models import Order
from products.models import Product
from sellers.models import Vendor
from rest_framework_simplejwt.tokens import RefreshToken

class VendorTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.register_url = reverse('register-vendor')
        self.login_url = reverse('login-vendor')
        self.vendor_customers_url = reverse('vendor-customers')
        self.update_url = reverse('update-vendor')
        self.user = User.objects.create_user(username='testuser', email='testuser@example.com', password='password')
        self.user2 = User.objects.create_user(username='testuser1', email='testuser2@example.com', password='password')

        session = self.client.session
        session.create()
        session_key = session.session_key

        self.vendor = Vendor.objects.create(user=self.user, username='testvendor', brand_name='testvendor', first_name='testvendor', last_name='testvendor', phone='+1234567890', address='testaddress', category='Office Supplies', brand_type='Physical Store', email='testvendor@example.com', city='testcity', state='testsate', country='testcountyr')
        self.vendor2 = Vendor.objects.create(user=self.user2, username='test1vendor', brand_name='test1vendor', first_name='testvendor', last_name='testvendor', phone='+1234567880', address='testaddress', category='Office Supplies', brand_type='Physical Store', email='testvendor2@example.com', city='testcity', state='testsate', country='testcountyr')
        self.customer1 = Customer.objects.create(user=self.user, first_name='Test', last_name='User', address='Test Address', phone='+254712345678', email='test_email@gmail.com')
        self.customer2 = Customer.objects.create(user=self.user2, first_name='Test2', last_name='User2', address='Test Address', phone='+254712345674', email='test_email2@gmail.com')

        # products
        self.product1 = Product.objects.create(name='Test Product', quantity=10, price=100.00, category='Men', product_type='Men sets', brand="Test_brand1", description="Test", vendor=self.vendor)
        self.product2 = Product.objects.create(name='Test Product2', quantity=10, price=100.00, category='Men', product_type='Men sets', brand="Test_brand2", description="Test", vendor=self.vendor2)

        # cart and cart items
        self.cart = Cart.objects.create(customer=self.customer1)
        self.cart2 = Cart.objects.create(customer=self.customer2)
        self.cart_item = CartItem.objects.create(cart=self.cart, product=self.product1, quantity=1)
        self.cart_item2 = CartItem.objects.create(cart=self.cart2, product=self.product2, quantity=1)
        
        # Orders
        self.order1 = Order.objects.create(customer=self.customer1, cart=self.cart)
        self.order2 = Order.objects.create(customer=self.customer2, cart=self.cart2)


    def test_register_vendor(self):
        data = {
            'username': 'newvendor',
            'email': 'newvendor@example.com',
            'password': 'Hustle247$',
            'first_name': 'New Vendor',
            'last_name': 'New Vendor',
            'brand_name': 'New Vendor',
            'phone': '+12345678902',
            'city': 'testcity',
            'address': 'testaddress',
            'country': 'testcountry',
            'brand_type': 'Physical Store',
            'category': 'Office Supplies',
            'state': 'anambra'

        }
        response = self.client.post(self.register_url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue('accessToken' in response.data['data'])

    def test_login_vendor(self):
        data = {
            'username': 'testuser',
            'password': 'password'
        }
        response = self.client.post(self.login_url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue('accessToken' in response.data['data'])

    def test_vendor_customers_view(self):
        self.client.login(username='testuser', password='password')
        response = self.client.get(self.vendor_customers_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    

    def test_update_vendor_view(self):
        data = {
            'first_name': 'Updated Vendor',
            'phone': '+12345678903',
            'city': 'Abuja',
            'email': 'updatedvendor@example.com'
        }
        self.client.login(username='testuser', password='password')
        response = self.client.patch(self.update_url, data, content_type='application/json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.vendor.refresh_from_db()
        self.assertEqual(self.vendor.first_name, 'Updated Vendor')
        self.assertEqual(self.vendor.email, 'updatedvendor@example.com')
