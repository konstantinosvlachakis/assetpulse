from rest_framework import serializers
from .models import Portfolio, Position


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