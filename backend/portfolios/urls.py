from django.urls import path
from .views import PortfolioListView, PortfolioDetailView

urlpatterns = [
   path("portfolios/", PortfolioListView.as_view(), name="portfolio-list"),
   path("portfolios/<int:id>/", PortfolioDetailView.as_view(), name="portfolio-detail"),
]

