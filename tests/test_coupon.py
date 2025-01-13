import json
from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User
from django.core.exceptions import ObjectDoesNotExist
from carts.models import Cart
from customers.models import Customer
from coupon.models import Coupon

class ApplyCouponViewTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username='testuser', password='testpassword')
        self.customer = Customer.objects.create(user=self.user, first_name='Test', last_name='User', address='Test Address', phone='+254712345678', email='test_email@gmail.com')
        self.cart = Cart.objects.create(customer=self.customer, total_amount=100)
        self.coupon = Coupon.objects.create(coupon_name='CHEELUX_TEST', code='TESTCOUPON', discount=0.1)
       
        self.url = reverse('apply-coupon')

    # def test_apply_coupon_success(self):
    #     # self.client.login(username='testuser', password='testpassword')
    #     response = self.client.post(self.url, json.dumps({'code': 'TESTCOUPON'}), content_type='application/json')
    #     print("Response JSON:", response.json())
    #     self.assertEqual(response.status_code, 200)
    #     self.assertEqual(response.json()['success'], True)
    #     self.assertEqual(response.json()['new_total'], 90.0)

    def test_apply_coupon_does_not_exist(self):
        self.client.login(username='testuser', password='testpassword')
        response = self.client.post(self.url, json.dumps({'code': 'INVALIDCOUPON'}), content_type='application/json')
       
        self.assertEqual(response.status_code, 404)
        self.assertEqual(response.json()['success'], False)
        self.assertEqual(response.json()['message'], 'Coupon does not exist')

    def test_apply_coupon_missing_code(self):
        self.client.login(username='testuser', password='testpassword')
        response = self.client.post(self.url, json.dumps({}), content_type='application/json')
      
        self.assertEqual(response.status_code, 404)
        self.assertEqual(response.json()['success'], False)
        self.assertEqual(response.json()['message'], 'Coupon does not exist')
