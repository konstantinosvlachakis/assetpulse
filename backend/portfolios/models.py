from django.db import models

from django.conf import settings

# Create your models here.

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