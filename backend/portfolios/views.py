from django.db import transaction
from django.db.models import Prefetch
from rest_framework.views import APIView
from rest_framework.response import Response

from assets.models import Asset

from .models import Portfolio, Position, Transaction
from .serializers import PortfolioSerializer, BuyPositionSerializer
# Create your views here.

class PortfolioListView(APIView):
    def get(self, request):
        portfolios = Portfolio.objects.prefetch_related(Prefetch("positions", queryset=Position.objects.select_related("asset")))
        serializer = PortfolioSerializer(portfolios, many=True)
        
        
        return  Response(serializer.data)

class PortfolioDetailView(APIView):
    def get(self, request, id):
        portfolio = (
            Portfolio.objects
            .prefetch_related(
                Prefetch(
                    "positions",
                    queryset=Position.objects.select_related("asset"),
                )
            )
            .get(id=id)
        )
        serializer = PortfolioSerializer(portfolio)
        
        return Response(serializer.data)
    
    

class PositionView(APIView):
    
    def post(self, request, id):
        
        portfolio = Portfolio.objects.get(id=id)
        serializer = BuyPositionSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        asset = serializer.validated_data["asset"]
        quantity = serializer.validated_data["quantity"]
        price = serializer.validated_data["price"]
       
        with transaction.atomic():
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
                
            Transaction.objects.create(
                asset=asset,
                type='buy',
                portfolio=portfolio,
                quantity=quantity,
                price=price
            )

        return Response({"message": "Position updated successfully."})