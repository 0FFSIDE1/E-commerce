import uuid
from django.test import TestCase, Client
from django.contrib.auth.models import User
from billings.models import Payment  
from django.conf import settings
from unittest.mock import patch

class PaymentViewTestCase(TestCase):
    def setUp(self):
        self.client = Client()

        # Create a test user and log them in
        self.user = User.objects.create_user(
            username="testuser", email="testuser@example.com", password="password123"
        )
        self.client.login(username="testuser", password="password123")

        # Example payment data
        self.payment_data = {
            "email": "payer@example.com",
            "amount": 1000.0,
        }

        # Example reference
        self.ref = "test-ref"

        # Mocked Paystack public key
        settings.PAYSTACK_PUBLIC_KEY = "test-public-key"

        # Mocked Payment object
        self.payment = Payment.objects.create(
            ref=self.ref, email=self.payment_data["email"], amount=self.payment_data["amount"], user=self.user
        )

    # @patch("billings.models.Payment.verify_payment")
    # def test_initiate_payment_success(self, mock_verify_payment):
    #     """Test successful payment initiation."""
    #     response = self.client.post("/api/v1/initiate/payment", self.payment_data, content_type="application/json")

    #     self.assertEqual(response.status_code, 201)
    #     self.assertTrue(response.json()["success"])
    #     self.assertIn("paystack_public_key", response.json())
    #     self.assertEqual(response.json()["ppaystack_public_key"], settings.PAYSTACK_PUBLIC_KEY)

    def test_initiate_payment_invalid_data(self):
        """Test payment initiation with invalid data."""
        invalid_data = {
            "email": "",  # Missing email
            "amount": -500,  # Invalid amount
        }
        response = self.client.post("/api/v1/initiate/payment", invalid_data, content_type="application/json")

        self.assertEqual(response.status_code, 400)
        self.assertFalse(response.json()["success"])
        self.assertIn("message", response.json())

    @patch("billings.models.Payment.verify_payment")
    def test_verify_payment_success(self, mock_verify_payment):
        """Test successful payment verification."""
        mock_verify_payment.return_value = True  # Simulate successful verification

        response = self.client.get(f"/api/v1/verify/{self.ref}/payment")

        self.assertEqual(response.status_code, 200)
        self.assertTrue(response.json()["success"])
        self.assertEqual(response.json()["message"], "Payment Successful, funds are now in your account.")

    @patch("billings.models.Payment.verify_payment")
    def test_verify_payment_failure(self, mock_verify_payment):
        """Test payment verification failure."""
        mock_verify_payment.return_value = False  # Simulate failed verification

        response = self.client.get(f"/api/v1/verify/{self.ref}/payment")

        self.assertEqual(response.status_code, 400)
        self.assertFalse(response.json()["success"])
        self.assertEqual(response.json()["message"], "Payment verification failed. Please contact support.")

    def test_verify_payment_not_found(self):
        """Test verification of a non-existent payment."""
        ref = uuid.uuid4()
        response = self.client.get(f"/api/v1/verify/{ref}/payment")

        self.assertEqual(response.status_code, 404)
        self.assertFalse(response.json()["success"])
        self.assertIn("not found", response.json()["message"])

    @patch("billings.models.Payment.verify_payment")
    def test_verify_payment_exception(self, mock_verify_payment):
        """Test exception during payment verification."""
        mock_verify_payment.side_effect = Exception("Test exception")  # Simulate exception

        response = self.client.get(f"/api/v1/verify/{self.ref}/payment")

        self.assertEqual(response.status_code, 500)
        self.assertFalse(response.json()["success"])
        self.assertIn("An error occurred", response.json()["message"])
