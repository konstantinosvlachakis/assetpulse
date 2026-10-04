from django.db.models import Prefetch
from rest_framework.views import APIView
from rest_framework.response import Response

from .models import Portfolio, Position
from .serializers import PortfolioSerializer
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