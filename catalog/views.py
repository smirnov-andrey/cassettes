from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404
from django.urls import reverse
from django.utils.translation import gettext
from django.utils.decorators import method_decorator
from django.views.generic import (DetailView, ListView, CreateView,
                                  TemplateView, UpdateView, )
from django.views.generic.edit import FormMixin

from catalog.forms import (CassetteCreateForm, CassetteImageForm,
                           CassetteImageAddonsForm, CassettePriceForm,
                           CassetteCommentForm)
from catalog.models import (CassetteCategory, CassetteBrand,
                            Cassette, CassetteTechnology, CassettesImage,
                            CassettePrice, CassetteComment)


class CassetteCategoryListView(TemplateView):
    """Список категорий в каталоге"""
    template_name = 'catalog/category-list.html'

    def get_context_data(self, **kwargs):
        queryset = CassetteCategory.published_objects.all()
        context = super().get_context_data(**kwargs)
        context['category_audio'] = queryset.filter(type=CassetteCategory.AUDIO)
        context['category_video'] = queryset.filter(type=CassetteCategory.VIDEO)
        return context


class CassetteCategoryDetailView(DetailView):
    """Страница категории в каталоге"""
    model = CassetteCategory
    template_name = 'catalog/category-detail.html'

    def get_object(self, queryset=None):
        return CassetteCategory.published_objects.get(slug=self.kwargs['slug'])

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['brand_list'] = CassetteBrand.published_objects.filter(cassettes__category=self.get_object()).distinct()
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
        context['brand'] = CassetteBrand.published_objects.get(slug=self.kwargs['brand_slug'])
        context['category'] = CassetteCategory.published_objects.get(slug=self.kwargs['slug'])
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
        return CassetteBrand.published_objects.get(slug=self.kwargs['slug'])


class TechnologyListView(ListView):
    """Список технологий"""
    model = CassetteTechnology
    template_name = 'catalog/technologies.html'
    context_object_name = 'technology_list'


class CassetteDetailView(FormMixin, DetailView):
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
        context['comments'] = CassetteComment.published_objects.filter(cassette=self.get_object())
        context['form'] = CassetteCommentForm(
            initial={
                'user': self.request.user,
                'cassette': self.object
            }
        )
        return context

    @method_decorator(login_required)
    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        if request.POST.get('form_name') == 'comment':
            form = self.get_form()
            if form.is_valid():
                return self.form_valid(form)
            else:
                return self.form_invalid(form)
        if request.POST.get('form_name') == 'collection':
            # if
            print('collection')
        return super().get(request, *args, **kwargs)

    def form_valid(self, form):
        form.save()
        return super(CassetteDetailView, self).form_valid(form)


class CassetteCreateView(LoginRequiredMixin, UserPassesTestMixin, CreateView):
    """Добавление кассеты"""
    model = Cassette
    form_class = CassetteCreateForm
    template_name = 'catalog/edit-cassette.html'

    def test_func(self):
        return self.request.user.is_moderator or self.request.user.is_superuser

    def get_success_url(self):
        return reverse('catalog:cassette', kwargs={'id': self.object.pk})

    def get_context_data(self, **kwargs):
        context = super(CassetteCreateView, self).get_context_data(**kwargs)
        # Translators: Catalog view title for page ('Добавить предмет')
        context['page_title'] = gettext('Add item')
        if self.request.POST:
            context['cassette_image_form'] = CassetteImageForm(self.request.POST, self.request.FILES)
            context['cassette_image_addons_form'] = CassetteImageAddonsForm(self.request.POST, self.request.FILES)
            context['cassette_price_form'] = CassettePriceForm(self.request.POST)
        else:
            context['cassette_image_form'] = CassetteImageForm()
            context['cassette_image_addons_form'] = CassetteImageAddonsForm()
            context['cassette_price_form'] = CassettePriceForm()
        return context

    def form_valid(self, form):
        context = self.get_context_data()
        cassette_price_form = context['cassette_price_form']
        cassette_image_form = context['cassette_image_form']
        cassette_image_addons_form = context['cassette_image_addons_form']
        if cassette_price_form.is_valid() and cassette_image_form.is_valid() and cassette_image_addons_form.is_valid():
            self.object = form.save(commit=False)
            self.object.user = self.request.user
            self.object.save()
            price_object = cassette_price_form.save(commit=False)
            price_object.cassette = self.object
            price_object.save()
            image_object = cassette_image_form.save(commit=False)
            image_object.cassette = self.object
            image_object.frequency_response = cassette_image_addons_form.cleaned_data['frequency_response']
            image_object.barcode = cassette_image_addons_form.cleaned_data['barcode']
            image_object.save()
        else:
            return self.render_to_response(self.get_context_data(form=form))
        return super().form_valid(form)


class CassetteUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    """Редактирование кассеты"""
    model = Cassette
    form_class = CassetteCreateForm
    template_name = 'catalog/edit-cassette.html'

    def test_func(self):
        return self.request.user.is_moderator or self.request.user.is_superuser

    def get_success_url(self):
        return reverse('catalog:cassette', kwargs={'id': self.object.pk})

    def get_context_data(self, **kwargs):
        image_instance, _ = CassettesImage.objects.get_or_create(cassette=self.object)
        price_instance, _ = CassettePrice.objects.get_or_create(cassette=self.object)
        context = super(CassetteUpdateView, self).get_context_data(**kwargs)
        # Translators: Catalog view title for page ('Редактировать предмет')
        context['page_title'] = gettext('Edit Item')
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
        return get_object_or_404(Cassette, id=self.kwargs['id'])

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
