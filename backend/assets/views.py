from rest_framework.response import Response
from rest_framework.views import APIView

# Create your views here.
from .models import Asset
from .serializers import AssetSerializer
from django.shortcuts import get_object_or_404

from market_data.tasks import sync_asset_prices
class AssetListView(APIView):
    def get(self, request, symbol= None):
        # Get all Asset objects for the specified asset from PostgreSQL database
        if symbol is not None:
            asset = get_object_or_404(Asset, symbol=symbol)
            serializer = AssetSerializer(asset)
        else:
            assets = Asset.objects.all()
            serializer = AssetSerializer(assets, many=True)

       
        return Response(serializer.data)
    
    
class AssetSyncView(APIView):
    def post(self, request, symbol):
        # Get the Asset object for the specified symbol
        get_object_or_404(Asset, symbol=symbol)

        # Call the sync_asset_prices task
        task = sync_asset_prices.delay(symbol)

        # Return a success response
        return Response(
            {
                "message": f"Sync queued for {symbol}.",
                "task_id": task.id,
            },
            status=202,
        )