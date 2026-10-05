from decimal import Decimal
from urllib import response

from django.test import TestCase
from django.contrib.auth import get_user_model
from rest_framework.test import APIClient
from unittest.mock import patch
# Create your tests here.


from .models import Portfolio, Position, Transaction
from assets.models import Asset
class BuyPositionTests(TestCase):
    
    def setUp(self):
        self.client = APIClient()
        
        User = get_user_model()
        self.user = User.objects.create_user(username="testuser", password="testpassword")
        self.portfolio = Portfolio.objects.create(user=self.user, name="Test Portfolio", type="main portfolio")
        self.aapl = Asset.objects.create(symbol="AAPL", name="Apple Inc.", asset_type="stock")
        self.googl = Asset.objects.create(symbol="GOOGL", name="Alphabet Inc.", asset_type="stock")
        self.position = Position.objects.create(portfolio=self.portfolio, asset=self.aapl, quantity=10, average_price=150)
        self.transaction = Transaction.objects.create(portfolio=self.portfolio, asset=self.aapl, type='buy', quantity=1, price=150)
        
        
        
    def test_buy_existing_position(self):
        response = self.client.post(f"/api/portfolios/{self.portfolio.id}/positions/buy/", {
            "asset": "AAPL",
            "quantity": 2,
            "price": 200
        }, format='json')
        self.assertEqual(response.status_code, 200)
        self.position.refresh_from_db()
        self.assertEqual(self.position.quantity, Decimal("12"))
        self.assertEqual(self.position.average_price, Decimal("158.3333"))
        
        
    def test_buy_new_position(self):
        response = self.client.post(f"/api/portfolios/{self.portfolio.id}/positions/buy/", {
            "asset": "GOOGL",
            "quantity": 2,
            "price": 250
        }, format='json')
        
        self.assertEqual(response.status_code, 200)
        
        new_position = Position.objects.get(
            portfolio = self.portfolio,
            asset = self.googl
        )
        self.assertEqual(new_position.quantity,Decimal("2"))
        self.assertEqual(new_position.average_price, Decimal("250"))
        
        
    
    def test_buy_with_negative_quantity(self):
        
        response = self.client.post(f"/api/portfolios/{self.portfolio.id}/positions/buy/", {
                    "asset": "AAPL",
                    "quantity": -2,
                    "price": 200
                }, format='json')
        
        self.assertEqual(response.status_code, 400)
        self.position.refresh_from_db()
        self.assertEqual(self.position.quantity, Decimal("10"))
        self.assertEqual(self.position.average_price, Decimal("150"))
        
        
        
    
    def test_buy_rolls_back_when_transaction_fails(self):
        # Simulate a failure by providing an invalid asset symbol
        
        transactions_before = Transaction.objects.count()
        
        with patch(
            "portfolios.views.Transaction.objects.create",
            side_effect=Exception("Simulated failure")
        ):
            with self.assertRaises(Exception):
                self.client.post(
                    f"/api/portfolios/{self.portfolio.id}/positions/buy/",
                    {
                        "asset": "AAPL",
                        "quantity": 2,
                        "price": 200,
                    },
                    format="json",
                )
                        
            
        self.position.refresh_from_db()

        self.assertEqual(
            self.position.quantity,
            Decimal("10")
        )

        self.assertEqual(
            Transaction.objects.count(),
            transactions_before
        )
        
        
    
    def test_sell_position(self):
        response = self.client.post(f"/api/portfolios/{self.portfolio.id}/positions/sell/", {
            "asset": "AAPL",
            "quantity": 3,
            "price": 200
        }, format='json')
        
        self.assertEqual(response.status_code, 200)
        self.position.refresh_from_db()
        self.assertEqual(self.position.quantity, Decimal("7"))
        self.assertEqual(self.position.average_price, Decimal("150"))
        
        self.assertEqual(Transaction.objects.filter(portfolio=self.portfolio, asset=self.aapl, type='sell').count(), 1)



    def test_sell_full_position(self):
        response = self.client.post(f"/api/portfolios/{self.portfolio.id}/positions/sell/", {
            "asset": "AAPL",
            "quantity": 10,
            "price": 200
        }, format='json')
        
        self.assertEqual(response.status_code, 200)
        self.assertFalse(Position.objects.filter(portfolio=self.portfolio, asset=self.aapl).exists())
        self.assertEqual(Transaction.objects.filter(portfolio=self.portfolio, asset=self.aapl, type='sell').count(), 1)
        
        
        
    def test_sell_more_than_available(self):
        response = self.client.post(f"/api/portfolios/{self.portfolio.id}/positions/sell/", {
            "asset": "AAPL",
            "quantity": 15,
            "price": 200
        }, format='json')
        
        self.assertEqual(response.status_code, 400)
        self.position.refresh_from_db()
        self.assertEqual(self.position.quantity, Decimal("10"))
        self.assertEqual(self.position.average_price, Decimal("150"))
        self.assertEqual(Transaction.objects.filter(portfolio=self.portfolio, asset=self.aapl, type='sell').count(), 0)