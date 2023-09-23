from django.contrib.postgres.aggregates import ArrayAgg
from django.db.models import F, OuterRef
from django.shortcuts import get_object_or_404
from django.views.generic import ListView


from .models import *
from users.models import User


class CollectionListView(ListView):
    template_name = 'collection_management/user-collection.html'

    def get_queryset(self):
        collector = get_object_or_404(
            User,
            id=self.kwargs['collector_id']
        )
        cassettes = Cassette.objects.filter(
            collections__user=collector
        ).distinct()
        for cassette in cassettes:
            cassette.conditions = Condition.objects.filter(
                collections__user=collector,
                collections__cassette=cassette,
            ).order_by('-id')
        return cassettes

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['collector'] = get_object_or_404(
            User,
            id=self.kwargs['collector_id']
        )
        context['title'] = 'Collection'
        context['show_condition'] = True
        return context


class WishlistListView(ListView):
    template_name = 'collection_management/user-collection.html'

    def get_queryset(self):
        collector = get_object_or_404(
            User,
            id=self.kwargs['collector_id'])
        cassettes = Cassette.objects.filter(wishlists__user=collector)
        return cassettes

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["collector"] = get_object_or_404(
            User, id=self.kwargs['collector_id'])
        context['title'] = 'Wishlist'
        context['show_condition'] = False
        return context


class ExchangeListView(ListView):
    template_name = 'collection_management/user-collection.html'

    def get_queryset(self):
        collector = get_object_or_404(User, id=self.kwargs['collector_id'])
        cassettes = Cassette.objects.filter(exchanges__user=collector)
        for cassette in cassettes:
            cassette.conditions = Condition.objects.filter(
                collections__user=collector,
                collections__cassette=cassette,
            ).order_by('-id')
        return cassettes

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["collector"] = get_object_or_404(
            User, id=self.kwargs['collector_id'])
        context['title'] = 'Exchange'
        context['show_condition'] = False
        return context


class SaleListView(ListView):
    template_name = 'collection_management/user-collection.html'

    def get_queryset(self):
        collector = get_object_or_404(User, id=self.kwargs['collector_id'])
        cassettes = Cassette.objects.filter(sales__user=collector)
        for cassette in cassettes:
            cassette.conditions = Condition.objects.filter(
                collections__user=collector,
                collections__cassette=cassette,
            ).order_by('-id')
        return cassettes

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["collector"] = get_object_or_404(User,
            id=self.kwargs['collector_id'])
        context['title'] = 'Sale'
        context['show_condition'] = False
        return context

