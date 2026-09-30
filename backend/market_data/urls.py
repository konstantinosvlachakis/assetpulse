from django.urls import path

from .views import PriceListView

urlpatterns = [
    path("prices/", PriceListView.as_view(), name="price-list"),
    path("prices/<str:symbol>/", PriceListView.as_view(), name="price-list-by-symbol"),
    
]
