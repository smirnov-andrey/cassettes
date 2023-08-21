from django.urls import path
from .views import CollectionListView, ExchangeListView, SaleListView, WishlistListView

app_name = 'lists'

urlpatterns = [
    path('collection/<int:collector_id>/', CollectionListView.as_view(), name='collection'),
    path('whishlist/<int:collector_id>/', WishlistListView.as_view(), name='whishlist'),
    path('exchange/<int:collector_id>/', ExchangeListView.as_view(), name='exchange'),
    path('sale/<int:collector_id>/', SaleListView.as_view(), name='sale'),
]