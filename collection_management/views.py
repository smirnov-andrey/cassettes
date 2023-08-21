from django.shortcuts import get_object_or_404
from django.views.generic import ListView


from .models import *
from users.models import User


class CollectionListView(ListView):
    template_name = 'collection_management/user-collection.html'

    def get_queryset(self):
        collector = get_object_or_404(
            User, id=self.kwargs['collector_id'])
        return Collection.objects.filter(user=collector)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["collector"] = get_object_or_404(
            User, id=self.kwargs['collector_id'])
        context['title'] = 'Collection'
        return context




class WishlistListView(ListView):
    template_name = 'collection_management/user-collection.html'

    def get_queryset(self):
        collector = get_object_or_404(User, id=self.kwargs['collector_id'])
        return Wishlist.objects.filter(user=collector)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["collector"] = get_object_or_404(
            User, id=self.kwargs['collector_id'])
        context['title'] = 'Wishlist'
        return context


class ExchangeListView(ListView):
    template_name = 'collection_management/user-collection.html'

    def get_queryset(self):
        collector = get_object_or_404(User, id=self.kwargs['collector_id'])
        return Exchange.objects.filter(user=collector)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["collector"] = get_object_or_404(
            User, id=self.kwargs['collector_id'])
        context['title'] = 'Exchange'
        return context


class SaleListView(ListView):
    template_name = 'collection_management/user-collection.html'

    def get_queryset(self):
        collector = get_object_or_404(User, id=self.kwargs['collector_id'])
        return Sale.objects.filter(user=collector)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["collector"] = get_object_or_404(User,
            id=self.kwargs['collector_id'])
        context['title'] = 'Sale'
        return context

