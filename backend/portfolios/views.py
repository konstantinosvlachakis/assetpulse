from django.db import transaction
from django.db.models import Prefetch
from django.shortcuts import get_object_or_404

from rest_framework.views import APIView
from rest_framework.response import Response

from assets.models import Asset

from .models import Portfolio, Position, Transaction
from .serializers import PortfolioSerializer, PositionTransactionSerializer
from rest_framework.exceptions import ValidationError

from rest_framework.permissions import IsAuthenticated

# Create your views here.

class PortfolioListView(APIView):
    def get(self, request):
        portfolios = Portfolio.objects.prefetch_related(Prefetch("positions", queryset=Position.objects.select_related("asset")))
        serializer = PortfolioSerializer(portfolios, many=True)
        
        
        return  Response(serializer.data)

class PortfolioDetailView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, id):
        user = request.user
        portfolio = get_object_or_404(
            Portfolio.objects
            .prefetch_related(
                Prefetch(
                    "positions",
                    queryset=Position.objects.select_related("asset"),
                )
            ),
            id=id,
            user=user,
        )
        serializer = PortfolioSerializer(portfolio)
        
        return Response(serializer.data)
    
    

class PositionView(APIView):
    
    permission_classes = [IsAuthenticated]
    
    def post(self, request, id, transaction_type):
        
        if transaction_type not in ['buy', 'sell']:
            raise ValidationError({"transaction_type": "Invalid transaction type. Must be 'buy' or 'sell'."})
        portfolio = get_object_or_404(Portfolio, id=id, user=request.user)
        serializer = PositionTransactionSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        asset_symbol = serializer.validated_data["asset"]
        quantity = serializer.validated_data["quantity"]
        price = serializer.validated_data["price"]
        asset = Asset.objects.get(symbol=asset_symbol)
       
        with transaction.atomic():
            if transaction_type == 'buy':
                position, created = Position.objects.select_for_update().get_or_create(
                    portfolio=portfolio,
                    asset=asset,
                    defaults={"quantity": quantity, "average_price": price},
                )
                if not created:
                    # Update the existing position
                    old_cost = position.average_price * position.quantity
                    new_cost = price * quantity
                    new_quantity = position.quantity + quantity
                    new_average_price = (old_cost + new_cost) / new_quantity
                    position.quantity = new_quantity
                    position.average_price = new_average_price
                    position.save()
                         
            else:
                position = Position.objects.select_for_update().get(
                    portfolio=portfolio,
                    asset=asset,
                )
                if quantity > position.quantity:
                    raise ValidationError(
                        {"quantity": "Selling quantity cannot exceed current position quantity."}
                    )
                position.quantity -= quantity
                if position.quantity == 0:
                    position.delete()
                else:
                    position.save()
                
            Transaction.objects.create(
                asset=asset,
                type=transaction_type,
                portfolio=portfolio,
                quantity=quantity,
                price=price
            )

        return Response({"message": "Position updated successfully."})
