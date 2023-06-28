from django.urls import reverse
from django.views.generic import DetailView, ListView, CreateView, UpdateView
from django.views.generic.edit import FormMixin

from catalog.forms import (CassetteCreateForm,CassetteImageForm,
                           CassetteImageAddonsForm, CassettePriceForm,
                           CassetteCommentForm)
from catalog.models import (CassetteCategory, CassetteBrand,
                            Cassette, CassetteTechnology, CassettesImage,
                            CassettePrice, CassetteComment)


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


class CassetteDetailView(DetailView, FormMixin):
    """Кассета"""
    model = Cassette
    template_name = 'catalog/cassette.html'
    form_class = CassetteCommentForm

    def get_success_url(self):
        return reverse('catalog:cassette', kwargs={'id': self.object.id})

    def get_object(self, queryset=None):
        return Cassette.objects.get(id=self.kwargs['id'])

    def get_context_data(self, **kwargs):
        context = super(CassetteDetailView, self).get_context_data(**kwargs)
        context['form'] = CassetteCommentForm(
            initial={
                'user': self.request.user,
                'cassette': self.object
            }
        )
        return context

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        form = self.get_form()
        if form.is_valid():
            return self.form_valid(form)
        else:
            return self.form_invalid(form)

    def form_valid(self, form):
        form.save()
        return super(CassetteDetailView, self).form_valid(form)


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
    # success_url = '/'

    def get_success_url(self):
        return reverse('catalog:cassette', kwargs={'id': self.object.pk})

    def get_context_data(self, **kwargs):
        image_instance, _ = CassettesImage.objects.get_or_create(cassette=self.object)
        price_instance, _ = CassettePrice.objects.get_or_create(cassette=self.object)
        context = super(CassetteUpdateView, self).get_context_data(**kwargs)
        if self.request.POST:
            context['cassette_image_form'] = CassetteImageForm(self.request.POST, self.request.FILES, instance=image_instance)
            context['cassette_image_addons_form'] = CassetteImageAddonsForm(self.request.POST, self.request.FILES, instance=image_instance)
            context['cassette_price_form'] = CassettePriceForm(self.request.POST, instance=price_instance)
        else:
            context['cassette_image_form'] = CassetteImageForm(instance=image_instance)
            context['cassette_image_addons_form'] = CassetteImageAddonsForm(instance=image_instance)
            context['cassette_price_form'] = CassettePriceForm(instance=price_instance)
        return context

    def get_object(self):
        return Cassette.objects.get(id=self.kwargs['id'])

    def form_valid(self, form):
        context = self.get_context_data()
        cassette_price_form = context['cassette_price_form']
        cassette_image_form = context['cassette_image_form']
        cassette_image_addons_form = context['cassette_image_addons_form']
        if cassette_price_form.is_valid() and cassette_image_form.is_valid() and cassette_image_addons_form.is_valid():
            cassette_price_form.save()
            cassette_image_form.save()
            cassette_image_addons_form.save()
        else:
            return self.render_to_response(self.get_context_data(form=form))

        return super().form_valid(form)


