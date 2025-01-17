import uuid
from django.test import TestCase, Client
from django.contrib.auth.models import User
from reviews.models import Product, Customer, ProductReview
import json

class CreateProductReviewTestCase(TestCase):
    def setUp(self):
        # Create test user
        self.user = User.objects.create_user(username='testuser', password='password', email='example@gmail.com')
        
        # Create test customer linked to the user
        self.customer = Customer.objects.create(user=self.user, first_name='Test', last_name='User', address='Test Address', phone='+254712345678', email='test_email@gmail.com')
        
        # Create test product
        self.product = Product.objects.create(name='Test Product', quantity=10, price=100.00, category='Men', product_type='Men sets', brand="Test_brand", description="Test")
        
        # Set up test client and login
        self.client = Client()
        self.client.login(username='testuser', password='password')
        
        self.url = f'/api/v1/product/{self.product.item_id}/review/create'  # Replace with your actual endpoint
    
    def test_create_product_review_success(self):
        """Test successful creation of a product review."""
        payload = {
            'message': 'Great product!',
            'rating': 5
        }
        response = self.client.post(self.url, data=json.dumps(payload), content_type='application/json')
        
        self.assertEqual(response.status_code, 201)
        response_data = response.json()
        self.assertTrue(response_data['success'])
        self.assertEqual(response_data['message'], 'Thanks for your review')
        self.assertEqual(response_data['status'], 'success')
        
        # Assert the review was created in the database
        review = ProductReview.objects.filter(customer=self.customer, product=self.product).first()
        self.assertIsNotNone(review)
        self.assertEqual(review.message, payload['message'])
        self.assertEqual(review.rating, payload['rating'])

    def test_create_product_review_invalid_product(self):
        """Test creating a review for a non-existent product."""
        pk = uuid.uuid4()
        invalid_url = f'/api/v1/product/{pk}/review/create'  # Non-existent product ID
        payload = {
            'message': 'This product does not exist.',
            'rating': 4
        }
        response = self.client.post(invalid_url, data=json.dumps(payload), content_type='application/json')
        
        self.assertEqual(response.status_code, 404)
        response_data = response.json()
        self.assertFalse(response_data['success'])
        self.assertEqual(response_data['message'], 'Error adding review try again later')
        self.assertEqual(response_data['status'], 'error')

    def test_create_product_review_missing_fields(self):
        """Test creating a review with missing fields in the payload."""
        payload = {
            'rating': 4  # Missing 'message'
        }
        response = self.client.post(self.url, data=json.dumps(payload), content_type='application/json')
        
        self.assertEqual(response.status_code, 404)
        response_data = response.json()
        self.assertFalse(response_data['success'])
        self.assertEqual(response_data['message'], 'Error adding review try again later')
        self.assertEqual(response_data['status'], 'error')

    def test_create_product_review_unauthenticated(self):
        """Test creating a review when the user is not authenticated."""
        self.client.logout()  # Ensure the user is logged out
        payload = {
            'message': 'Great product!',
            'rating': 5
        }
        response = self.client.post(self.url, data=json.dumps(payload), content_type='application/json')
        
        self.assertEqual(response.status_code, 302)  # redirect to login page
