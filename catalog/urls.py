from django.urls import path
from .views import CassetteCategoryDetailView, CassetteCategoryListView, CassetteBrandListView, CassetteBrandDetail, \
    CassetteCatalogBrandDetailView, TechnologyListView, CassetteDetailView, CassetteCreateView, CassetteUpdateView

app_name = 'catalog'

urlpatterns = [
    path('', CassetteCategoryListView.as_view(), name='catalog-list'),
    path('category/<slug>/<brand_slug>/', CassetteCatalogBrandDetailView.as_view(), name='catalog-brand-cassette-list'),
    path('category/<slug>/', CassetteCategoryDetailView.as_view(), name='catalog-detail'),
    path('brands/', CassetteBrandListView.as_view(), name='brand-list'),
    path('brands/<slug>/', CassetteBrandDetail.as_view(), name='brand-detail'),
    path('technology/', TechnologyListView.as_view(), name='technologies'),
    path('cassettes/<int:id>/', CassetteDetailView.as_view(), name='cassette'),
    path('cassettes/add/', CassetteCreateView.as_view(), name='cassette_create'),
    path('cassettes/update/<int:id>', CassetteUpdateView.as_view(), name='cassette_update'),
]
