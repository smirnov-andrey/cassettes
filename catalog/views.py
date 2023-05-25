from django.db.models import Min, Max
from django.shortcuts import render
from django.views.generic import DetailView, ListView, CreateView, UpdateView

from catalog.forms import CassetteCreateForm, CassetteBarcodeFormSet, \
    CassetteFrequencyResponseFormSet, CassetteImageFormSet, CassettePriceFormSet
from catalog.models import CassetteCategory, CassetteBrand, Cassette, CassetteTechnology


class CassetteCategoryListView(ListView):
    """Список категорий в каталоге"""
    model = CassetteCategory
    template_name = 'catalog/category-list.html'
    context_object_name = 'category_list'


class CassetteCategoryDetailView(DetailView):
    """Страница категории в каталоге"""
    model = CassetteCategory
    template_name = 'catalog/category-detail.html'

    def get_object(self, queryset=None):
        return CassetteCategory.objects.get(slug=self.kwargs['slug'])

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['brand_list'] = CassetteBrand.objects.filter(cassettes__category=self.get_object()).distinct()
        return context


class CassetteCatalogBrandDetailView(ListView):
    """Список всех кассет конкретного бренда конкретной категории"""
    model = Cassette
    template_name = 'catalog/category-brand-cassette-list.html'
    context_object_name = 'cassette_list'

    def get_queryset(self):
        return Cassette.objects.filter(category__slug=self.kwargs['slug'], brand__slug=self.kwargs['brand_slug'])

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(CassetteCatalogBrandDetailView, self).get_context_data(**kwargs)
        context['brand'] = CassetteBrand.objects.get(slug=self.kwargs['brand_slug'])
        context['category'] = CassetteCategory.objects.get(slug=self.kwargs['slug'])
        return context


class CassetteBrandListView(ListView):
    """Список всех брендов в каталоге"""
    model = CassetteBrand
    template_name = 'catalog/brand-list.html'
    context_object_name = 'brand_list'


class CassetteBrandDetail(DetailView):
    """Детальная страница бренда общего каталога"""
    model = CassetteBrand
    template_name = 'catalog/brand-detail.html'
    context_object_name = 'brand'

    def get_object(self, queryset=None):
        return CassetteBrand.objects.get(slug=self.kwargs['slug'])


class TechnologyListView(ListView):
    """Список технологий"""
    model = CassetteTechnology
    template_name = 'catalog/technologies.html'
    context_object_name = 'technology_list'


class CassetteDetailView(DetailView):
    """Кассета"""
    model = Cassette
    template_name = 'catalog/cassette.html'

    def get_object(self, queryset=None):
        return Cassette.objects.get(id=self.kwargs['id'])


class CassetteCreateView(CreateView):
    """Добавление кассеты"""
    model = Cassette
    form_class = CassetteCreateForm
    template_name = 'catalog/add-cassette.html'


class CassetteUpdateView(UpdateView):
    """Редактирование кассеты"""
    model = Cassette
    form_class = CassetteCreateForm
    template_name = 'catalog/update-cassette.html'
    success_url = '/'

    def get_context_data(self, **kwargs):
        data = super(CassetteUpdateView, self).get_context_data(**kwargs)
        if self.request.POST:
            data['cassetteimageformset'] = CassetteImageFormSet(self.request.POST)
            data['cassettebarcodeformset'] = CassetteBarcodeFormSet(self.request.POST)
            data['cassetteresponceformset'] = CassetteFrequencyResponseFormSet(self.request.POST)
            data['cassettepriceformset'] = CassettePriceFormSet(self.request.POST)
        else:
            data['cassetteimageformset'] = CassetteImageFormSet()
            data['cassettebarcodeformset'] = CassetteBarcodeFormSet()
            data['cassetteresponceformset'] = CassetteFrequencyResponseFormSet()
            data['cassettepriceformset'] = CassettePriceFormSet()
        return data

    def get_object(self, queryset=None):
        return Cassette.objects.get(id=self.kwargs['id'])


