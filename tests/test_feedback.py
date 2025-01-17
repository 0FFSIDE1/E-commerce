from django.urls import reverse
from django.test import TestCase, Client
from feedbacks.models import Feedback

class FeedbackTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.create_feedback_url = reverse('create-feedbacks')  # Replace 'create-feedback' with your actual URL name.
        self.valid_payload = {
            "email": "testuser@example.com",
            "message": "This is a test feedback message."
        }
        self.invalid_payload = {
            "email": "",
            
        }

    def test_create_feedback_success(self):
        """Test successfully creating feedback."""
        response = self.client.post(
            self.create_feedback_url, 
            data=self.valid_payload, 
            content_type="application/json"
        )

        # Assert response status code
        self.assertEqual(response.status_code, 201)

        # Assert response data
        data = response.json()
        self.assertTrue(data['success'])
        self.assertEqual(data['message'], 'Thanks for your feedback. We appreciate your response!')

        # Assert that feedback was created
        self.assertEqual(Feedback.objects.count(), 1)
        feedback = Feedback.objects.first()
        self.assertEqual(feedback.email, self.valid_payload['email'])
        self.assertEqual(feedback.message, self.valid_payload['message'])

    def test_create_feedback_invalid_payload(self):
        """Test creating feedback with invalid payload."""
        response = self.client.post(
            self.create_feedback_url, 
            data=self.invalid_payload, 
            content_type="application/json"
        )

        # Assert response status code
        self.assertEqual(response.status_code, 400)

        # Assert response data
        data = response.json()
        self.assertFalse(data['success'])
        self.assertIn('Message field is required.', data['message'])

        # Assert that no feedback was created
        self.assertEqual(Feedback.objects.count(), 0)

    def test_create_feedback_missing_fields(self):
        """Test creating feedback with missing fields."""
        response = self.client.post(
            self.create_feedback_url, 
            data={"email": "onlyemail@example.com"}, 
            content_type="application/json"
        )

        # Assert response status code
        self.assertEqual(response.status_code, 400)

        # Assert response data
        data = response.json()
        self.assertFalse(data['success'])
        self.assertIn('Message field is required.', data['message'])

        # Assert that no feedback was created
        self.assertEqual(Feedback.objects.count(), 0)
