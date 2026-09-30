from django.urls import path
from .views import AssetListView, AssetSyncView

urlpatterns = [
    path("assets/", AssetListView.as_view(), name="asset-list"),
    path("assets/<str:symbol>/", AssetListView.as_view(), name="asset-list-by-symbol"),
    path("assets/<str:symbol>/sync/", AssetSyncView.as_view(), name="asset-sync-by-symbol"),
]

