from rest_framework.response import Response
from rest_framework.views import APIView
from django.shortcuts import get_object_or_404


from assets.models import Asset
from .models import Price
from .serializers import PriceSerializer


# Create your views here.

class PriceListView(APIView):
    def get(self, request, symbol= None):
        # Get all Price objects for the specified asset from PostgreSQL database
        if symbol is not None:
            asset = get_object_or_404(Asset, symbol=symbol)
            prices = asset.prices.all()
        else:
            prices = Price.objects.all()

        # Serialize the Price objects using the PriceSerializer
        serializer = PriceSerializer(prices, many=True)
        return Response(serializer.data)
    
    
    