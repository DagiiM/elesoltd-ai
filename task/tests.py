from django.test import TestCase

# Create your tests here.
from django.test import TestCase
from .models import Order

class CheckoutTestCase(TestCase):
    def test_form_submission(self):
        # Submit form
        response = self.client.post("/checkout/", {
            "name": "John Smith",
            "email": "john@example.com",
            "phone": "123-456-7890",
            "address": "123 Main St",
            "city": "New York",
            "state": "NY",
            "zip-code": "10001",
            "card-number": "4111 1111 1111 1111",
            "expiration-date": "01/23",
            "cvv": "123",
        })
        
        # Check that form was submitted successfully
        self.assertEqual(response.status_code, 200)
        
        # Check that order was saved to database
        self.assertEqual(Order.objects.count(), 1)
        order = Order.objects.first()
        self.assertEqual(order.name, "John Smith")
        self.assertEqual(order.email, "john@example.com")
        self.assertEqual(order.phone, "123-456-7890")
        self.assertEqual(order.address, "123 Main St")
        self.assertEqual(order.city, "New York")
        self.assertEqual(order.state, "NY")
        self.assertEqual(order.zip_code, "10001")
        self.assertEqual(order.card_number, "4111 1111 1111 1111")
        self.assertEqual(order.expiration_date, "01/23")
        self.assertEqual(order.cvv, "123")
