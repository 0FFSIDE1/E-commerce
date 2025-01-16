import uuid
from django.urls import reverse
from wishlist.models import Wishlist, WishlistItem
from products.models import Product
from django.test import TestCase, Client
from django.contrib.auth import get_user_model
User = get_user_model()

class WishlistTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username='testuser', email='testuser@example.com', password='password')
        self.product = Product.objects.create(name='Test Product', quantity=10, price=100.00, category='Men', product_type='Men sets', brand="Test_brand", description="Test")
        self.add_to_wishlist_url = reverse('add-to-wishlist', kwargs={'pk': self.product.item_id})
        self.get_wishlist_url = reverse('get-wishlist')
        self.client.login(username='testuser', password='password')

    def test_add_to_wishlist(self):
        response = self.client.post(self.add_to_wishlist_url)
        self.assertEqual(response.status_code, 201)
        self.assertTrue(WishlistItem.objects.filter(wishlist__user=self.user, product=self.product).exists())
    
    def test_get_wishlist(self):
        wishlist = Wishlist.objects.create(user=self.user)
        product =  Product.objects.create(name='Test# Product', quantity=10, price=100.00, category='Men', product_type='Men sets', brand="Test_brand#", description="Test")
        WishlistItem.objects.create(wishlist=wishlist, product=product)

        response = self.client.get(self.get_wishlist_url)
        self.assertEqual(response.status_code, 200)
        self.assertTrue('wishlist_items' in response.json())
        self.assertEqual(len(response.json()['wishlist_items']), 1)

    def test_add_to_wishlist_product_not_found(self):
        invalid_uuid = uuid.uuid4()
        invalid_url = reverse('add-to-wishlist', kwargs={'pk': invalid_uuid})
        response = self.client.post(invalid_url)
        self.assertEqual(response.status_code, 404)
        self.assertFalse(WishlistItem.objects.filter(wishlist__user=self.user, product__pk=999).exists())

    

    def test_get_wishlist_does_not_exist(self):
        """Test retrieving wishlist when no wishlist exists for the user."""
        # Log in as a different user without a wishlist
        new_user = User.objects.create_user(username='newuser', password='newpassword')
        self.client.login(username='newuser', password='newpassword')

        url = reverse('get-wishlist')
        response = self.client.get(url)

        # Check status code
        self.assertEqual(response.status_code, 404)

        # Check response data
        data = response.json()
        self.assertFalse(data['success'])
        self.assertEqual(data['message'], 'Wishlist does not exist for the user')

    def test_get_wishlist_server_error(self):
        """Test handling of unexpected errors."""
        # Simulate an exception by deleting the wishlist after setup
        Wishlist.objects.filter(user=self.user).delete()

        url = reverse('get-wishlist')
        response = self.client.get(url)

        # Check status code
        self.assertEqual(response.status_code, 404)

        # Check response data
        data = response.json()
        self.assertFalse(data['success'])
        self.assertEqual(data['message'], 'Wishlist does not exist for the user')
