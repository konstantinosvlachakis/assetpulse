from django.db import models

ASSET_TYPES = [
    ("stock", "Stock"), ("crypto", "Crypto")]

# Create your models here.
class Asset(models.Model):
    
    symbol = models.CharField(max_length=10, unique=True)
    name = models.CharField(max_length=30)
    asset_type = models.CharField(max_length=20, choices=ASSET_TYPES)
    
    def __str__(self):
        return self.symbol
    
    
    
    