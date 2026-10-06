from django.core.cache import cache
from rest_framework.response import Response
from rest_framework.views import APIView
from django.shortcuts import get_object_or_404


from assets.models import Asset
from .models import Price
from .serializers import PriceSerializer



class PriceListView(APIView):
    def get(self, request, symbol= None):
        
        if symbol:
            key = f"market_data:prices:{symbol}:latest"
        else:
            key = "market_data:prices:all"
                
        data = cache.get(key)
        
        if data is not None:
            return Response(data)

        # Get all Price objects for the specified asset from PostgreSQL database
        if symbol is not None:
            asset = get_object_or_404(Asset, symbol=symbol)
            prices = asset.prices.all()
        else:
            prices = Price.objects.all()

        # Serialize the Price objects using the PriceSerializer
        serializer = PriceSerializer(prices, many=True)
        cache.set(key, serializer.data, timeout=60 * 5)  # Cache for 5 minutes
        
      
        return Response(serializer.data)
    
    
    