from django.db import models

from django.conf import settings

import uuid

# Create your models here.
TRANSACTION_TYPES=[
    ('buy', 'Buy'),
    ('sell', 'Sell'),
]

class Portfolio(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="portfolios")
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    type = models.CharField(max_length=50, choices=[('main portfolio', 'Main Portfolio'), ('long term', 'Long Term'), ('short term', 'Short Term')], default='Main Portfolio' )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name
    
    
    

class Position(models.Model):
    asset = models.ForeignKey('assets.Asset', on_delete=models.PROTECT, related_name='positions')
    quantity = models.DecimalField(max_digits=20, decimal_places=4)
    average_price = models.DecimalField(max_digits=20, decimal_places=4)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    portfolio = models.ForeignKey(Portfolio, on_delete=models.CASCADE, related_name='positions')
    
    
    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['asset', 'portfolio'], name='unique_position_per_portfolio')
        ]

    def __str__(self):
        return f"{self.quantity} of {self.asset.symbol}"
    
    
    


class Transaction(models.Model):
    asset = models.ForeignKey('assets.Asset', on_delete=models.PROTECT, related_name='transactions')
    type =  models.CharField(max_length=4, choices=TRANSACTION_TYPES)
    portfolio = models.ForeignKey(Portfolio, on_delete=models.CASCADE, related_name='transactions')
    quantity = models.DecimalField(max_digits=20, decimal_places=4)
    price = models.DecimalField(max_digits=20, decimal_places=4)
    created_at = models.DateTimeField(auto_now_add=True)
    idempotency_key = models.UUIDField(unique=True, null=True)
    
    class Meta:
        constraints = [
            models.CheckConstraint(
                check=models.Q(quantity__gt=0),
                name="quantity_positive",
            ),
            models.CheckConstraint(
                check=models.Q(price__gt=0),
                name="price_positive",
            ),
        ]

        indexes = [
            models.Index(
                fields=["portfolio", "-created_at"],
                name="portfolio_created_idx",
            ),
        ]
        
    def __str__(self):
        return f"{self.type} {self.quantity} of {self.asset.symbol} at {self.price}"