from rest_framework.views import APIView
from rest_framework.response import Response

from .models import Portfolio
# Create your views here.

class PortfolioListView(APIView):
    def get(self, request):
        portfolios = Portfolio.objects.all()
        return  Response([{
                    "id": portfolio.id,
                    "name": portfolio.name,
                } for portfolio in portfolios])

class PortfolioDetailView(APIView):
    def get(self, request, id):
        portfolio = Portfolio.objects.get(id=id)

        return Response({
            "id": portfolio.id,
            "name": portfolio.name,
        })