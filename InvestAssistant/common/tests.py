from django.test import TestCase, Client
from django.urls import reverse
from InvestAssistant.instruments.models import Instrument

from decimal import Decimal


class TestHomePageView(TestCase):
    def setUp(self):
        self.client = Client()
        self.url = reverse('home')
        self.instrument1 = Instrument.objects.create(
            name="Apple Inc",
            ticker="AAPL",
            current_price=Decimal('150.00')
        )
        self.instrument2 = Instrument.objects.create(
            name="Microsoft",
            ticker="MSFT",
            current_price=Decimal('300.00')
        )

    def test_home_page_get(self):
        """Test HomePage view GET request"""
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'common/home-dashboard.html')
        self.assertIn('instruments', response.context)

    def test_search_functionality(self):
        """Test search functionality in HomePage"""

        response = self.client.get(f"{self.url}?q=Apple")
        self.assertIn(self.instrument1, response.context['instruments'])
        self.assertNotIn(self.instrument2, response.context['instruments'])

        response = self.client.get(f"{self.url}?q=MSFT")
        self.assertIn(self.instrument2, response.context['instruments'])
        self.assertNotIn(self.instrument1, response.context['instruments'])

    def test_pagination(self):
        """Test pagination of instruments"""
        # Create more instruments to test pagination
        for i in range(7): 
            Instrument.objects.create(
                name=f"Test Instrument {i}",
                ticker=f"TEST{i}",
                current_price=Decimal('100.00')
            )

        response = self.client.get(self.url)
        self.assertEqual(len(response.context['instruments']), 6)  # Check first page has 6 items

        response = self.client.get(f"{self.url}?page=2")
        self.assertEqual(response.status_code, 200)  # Check second page exists

