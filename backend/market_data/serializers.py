from rest_framework import serializers
from .models import Price


class PriceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Price
        fields = ["id", "asset", "date", "open_price", "high_price", "low_price", "close_price"]
        
        