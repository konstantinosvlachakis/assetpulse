from django.urls import path
from .views import PortfolioListView, PortfolioDetailView, PositionView

urlpatterns = [
   path("portfolios/", PortfolioListView.as_view(), name="portfolio-list"),
   path("portfolios/<int:id>/", PortfolioDetailView.as_view(), name="portfolio-detail"),
   path("portfolios/<int:id>/positions/<str:transaction_type>/", PositionView.as_view(), name="position-buy"),
]

