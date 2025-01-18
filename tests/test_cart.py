from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User
from carts.models import Cart, CartItem
from products.models import Product
import uuid
from customers.models import Customer
from sellers.models import Vendor

class CartTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username='testuser', password='testpassword')
        self.vendor = Vendor.objects.create(user=self.user, username='testvendor', brand_name='testvendor', first_name='testvendor', last_name='testvendor', phone='+1234567890', address='testaddress', category='Office Supplies', brand_type='Physical Store', email='testvendor@example.com', city='testcity', state='testsate', country='testcountyr')
        self.product = Product.objects.create(name='Test Product', quantity=10, price=100.00, category='Men', product_type='Men sets', brand="Test_brand", description="Test", vendor=self.vendor)
        self.customer = Customer.objects.create(user=self.user, first_name='Test', last_name='User', address='Test Address', phone='+254712345678', email='test_email@gmail.com')
        self.cart = Cart.objects.create(customer=self.customer)
        self.add_to_cart_url = reverse('add-to-cart', args=[self.product.pk])
        self.cart_item = CartItem.objects.create(cart=self.cart, product=self.product, quantity=1)
        self.get_cart_url = reverse('get-cart')

    def test_add_to_cart_success(self):
        self.client.login(username='testuser', password='testpassword')
        response = self.client.post(self.add_to_cart_url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()['success'], True)
        self.assertEqual(response.json()['message'], 'Test Product added to cart successfully!')
        self.assertEqual(response.json()['product']['name'], self.product.name)
        self.assertEqual(response.json()['product']['quantity'], self.product.quantity)
        self.assertEqual(response.json()['product']['price'], self.product.price)

    def test_add_to_cart_product_not_found(self):
        self.client.login(username='testuser', password='testpassword')
        invalid_product_url = reverse('add-to-cart', args=[uuid.uuid4()])
        response = self.client.post(invalid_product_url)
        self.assertEqual(response.status_code, 500)
        self.assertEqual(response.json()['success'], False)
        self.assertEqual(response.json()['message'], 'An error occurred. Please try again.')

    def test_add_to_cart_out_of_stock(self):
        self.client.login(username='testuser', password='testpassword')
        self.product.quantity = 0
        self.product.save()
        response = self.client.post(self.add_to_cart_url)
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json()['success'], False)
        self.assertEqual(response.json()['message'], 'Product is out of stock.')

    def test_add_to_cart_cart_not_found_and_create_a_new_cart(self):
        self.client.login(username='testuser', password='testpassword')
        Cart.objects.filter(customer=self.customer).delete()
        response = self.client.post(self.add_to_cart_url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()['success'], True)
        self.assertEqual(response.json()['message'], 'Test Product added to cart successfully!')

    def test_add_to_cart_unauthenticated(self):
        response = self.client.post(self.add_to_cart_url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()['message'], 'Test Product added to cart successfully!')
        self.assertEqual(response.json()['product']['name'], self.product.name)
        self.assertEqual(response.json()['product']['quantity'], self.product.quantity)
        self.assertEqual(response.json()['product']['price'], self.product.price)  

    
    def test_get_cart_success(self):
        self.client.login(username='testuser', password='testpassword')
        response = self.client.get(self.get_cart_url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()['success'], True)
        self.assertEqual(response.json()['message'], 'Cart retrieved successfully')
        self.assertEqual(len(response.json()['cartitems']), 0)
        

    def test_get_cart_unauthenticated(self):
        response = self.client.get(self.get_cart_url)
        self.assertEqual(response.status_code, 200)  
        self.assertEqual(response.json()['success'], True)
        self.assertEqual(response.json()['message'], 'Cart retrieved successfully')

    def test_get_cart_anonymous_user(self):
        session = self.client.session
        session.create()
        session_key = session.session_key
        self.cart.session = session_key
        self.cart.save()
        response = self.client.get(self.get_cart_url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()['success'], True)
        self.assertEqual(response.json()['message'], 'Cart retrieved successfully')
        self.assertEqual(len(response.json()['cartitems']), 0)
        







   
