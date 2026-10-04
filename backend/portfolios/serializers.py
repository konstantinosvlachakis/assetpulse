from rest_framework import serializers
from .models import Portfolio, Position
from decimal import Decimal



class PositionSerializer(serializers.ModelSerializer):
    asset = serializers.CharField(source="asset.symbol", read_only=True)

    class Meta:
        model = Position
        fields = ["asset", "quantity", "average_price"]


class PortfolioSerializer(serializers.ModelSerializer):
    positions = PositionSerializer(many=True, read_only=True)

    class Meta:
        model = Portfolio
        fields = ["id", "name", "description", "type", "positions", "created_at", "updated_at"]
        
        
        


class BuyPositionSerializer(serializers.Serializer):
    asset = serializers.CharField()
    quantity = serializers.DecimalField(min_value=Decimal("0.0001"), max_digits=20, decimal_places=4)
    price = serializers.DecimalField(max_digits=20, decimal_places=4, min_value=Decimal("0.0001"))
    
    