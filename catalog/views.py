from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.decorators import login_required
from django.db.models.functions import Coalesce
from django.db.models import F, Count, Subquery, OuterRef, Min, Max
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse
from django.utils.translation import gettext
from django.utils.decorators import method_decorator
from django.views.generic import (DetailView, ListView, CreateView,
                                  TemplateView, UpdateView, )
from django.views.generic.edit import FormMixin

from catalog.forms import (CassetteCreateForm, ImageForm, ImageFormSet,
                           CassettePriceForm,
                           CassetteCommentForm)
from catalog.models import (Category, CassetteBrand,
                            Cassette, CassetteTechnology, Image,
                            CassettePrice, CassetteComment, Condition)
from collection_management.models import Collection, Wishlist, Exchange, Sale


class CategoryListView(TemplateView):
    """Список категорий в каталоге"""
    template_name = 'catalog/category-list.html'

    def get_context_data(self, **kwargs):
        queryset = Category.published_objects.all()
        context = super().get_context_data(**kwargs)
        context['category_audio'] = queryset.filter(type=Category.AUDIO)
        context['category_video'] = queryset.filter(type=Category.VIDEO)
        return context


class CategoryDetailView(DetailView):
    """Страница категории в каталоге"""
    model = Category
    template_name = 'catalog/category-detail.html'
    # queryset = Category.objects.prefetch_related(
    #     'brands'
    # ).filter(is_published=True)

    def get_object(self, queryset=None):
        return Category.published_objects.get(slug=self.kwargs['slug'])

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['brand_list'] = CassetteBrand.published_objects.select_related(
            'country',
        ).filter(
            cassettes__category=self.get_object()
        ).annotate(
            cassette_count=Count('cassettes'),
            year_min=Min('cassettes__year_release'),
            year_max=Max('cassettes__year_release'),
        ).distinct()
        return context


class CassetteCatalogBrandDetailView(ListView):
    """Список всех кассет конкретного бренда конкретной категории"""
    model = Cassette
    template_name = 'catalog/category-brand-cassette-list.html'
    context_object_name = 'cassette_list'

    def get_queryset(self):
        return Cassette.objects.prefetch_related(
            'images', 'markets'
        ).select_related(
            'category', 'brand', 'tape_type', 'model', 'technology',
            'manufacturer', 'series', 'sort', 'tape_length', 'country'
        ).filter(
            category__slug=self.kwargs['slug'],
            brand__slug=self.kwargs['brand_slug']
        )

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(CassetteCatalogBrandDetailView, self).get_context_data(**kwargs)
        context['brand'] = CassetteBrand.published_objects.get(slug=self.kwargs['brand_slug'])
        context['category'] = Category.published_objects.get(slug=self.kwargs['slug'])
        return context


class CassetteBrandListView(ListView):
    """Список всех брендов в каталоге"""
    # model = CassetteBrand
    template_name = 'catalog/brand-list.html'
    context_object_name = 'brand_list'
    queryset = CassetteBrand.objects.annotate(
        cassette_count=Count('cassettes'),
        year_min=Min('cassettes__year_release'),
        year_max=Max('cassettes__year_release'),
    ).filter(is_published=True)



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
        return Cassette.objects.prefetch_related(
            'images', 'markets'
        ).select_related(
            'category', 'brand', 'tape_type', 'model', 'technology',
            'manufacturer', 'series', 'sort', 'tape_length', 'country'
        ).get(id=self.kwargs['id'])

    def get_context_data(self, **kwargs):
        context = super(CassetteDetailView, self).get_context_data(**kwargs)
        context['price'] = CassettePrice.objects.get_or_create(
            cassette=self.object
        )
        context['images'] = self.object.images.exclude(
            view=Image.View.BARCODE).exclude(
            view=Image.View.FREQUENCY_RESPONSE).order_by('view')
        context['barcode'] = self.object.images.filter(
            view=Image.View.BARCODE).first()
        context['frequency_response'] = self.object.images.filter(
            view=Image.View.FREQUENCY_RESPONSE).first()
        if self.request.user.is_authenticated:
            collection_queryset = self.request.user.collections.filter(
                cassette=self.object
            )
            exchange_queryset = self.request.user.exchanges.filter(
                cassette=self.object
            )
            sell_queryset = self.request.user.sales.filter(
                cassette=self.object
            )

            condition_in_collection = []
            for cassete in collection_queryset:
                condition_in_collection.append(cassete.condition.name)
            context['conditions_set'] = condition_in_collection
            context['is_in_collection'] = collection_queryset.exists()
            context['is_in_exchange'] = exchange_queryset.exists()
            context['is_in_sell'] = sell_queryset.exists()
            context['is_in_wishlist'] = self.request.user.wishlists.filter(
                cassette=self.object).exists()
            context['form'] = CassetteCommentForm(
                initial={'user': self.request.user, 'cassette': self.object}
            )
        context['comments'] = CassetteComment.published_objects.filter(
            cassette=self.get_object())

        return context

    @method_decorator(login_required)
    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        context = self.get_context_data()
        checkboxes = request.POST.getlist('collections')
        conditions = request.POST.getlist('conditions')
        if (request.POST.get('form_name')
                and request.POST.get('form_name') == 'collection'):
            if conditions:
                for condition in Condition.objects.all():
                    if condition.name in conditions:
                        obj, created = Collection.objects.get_or_create(
                            user=self.request.user,
                            cassette=self.object,
                            condition=condition
                        )
                        if created and request.POST.get('price-collection'):
                            obj.price = int(request.POST.get('price-collection'))
                            obj.save()
            Collection.objects.filter(
                user=self.request.user,
                cassette=self.object,
            ).exclude(
                condition__name__in=conditions
            ).delete()
        elif (request.POST.get('form_name')
                and request.POST.get('form_name') == 'lists'):
            if 'wishlist' in checkboxes:
                Wishlist.objects.get_or_create(user=self.request.user,
                                               cassette=self.object)
            else:
                Wishlist.objects.filter(
                    user=self.request.user,
                    cassette=self.object
                ).delete()
            if 'exchange' in checkboxes:
                Exchange.objects.get_or_create(user=self.request.user,
                                               cassette=self.object)
            else:
                Exchange.objects.filter(
                    user=self.request.user,
                    cassette=self.object
                ).delete()
            if 'sell' in checkboxes:
                Sale.objects.get_or_create(user=self.request.user,
                                           cassette=self.object)
            else:
                Sale.objects.filter(
                    user=self.request.user,
                    cassette=self.object
                ).delete()
        if request.POST.get('form_name') == 'comment':
            form = self.form_class(request.POST)
            if form.is_valid():
                return self.form_valid(form)
            else:
                return self.form_invalid(form)
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
            context['imageformset'] = ImageFormSet(self.request.POST)
            # context['cassette_image_form'] = CassetteImageForm(self.request.POST, self.request.FILES)
            # context['cassette_image_addons_form'] = CassetteImageAddonsForm(self.request.POST, self.request.FILES)
            context['cassette_price_form'] = CassettePriceForm(self.request.POST)
        else:
            context['imageformset'] = ImageFormSet()
            # context['cassette_image_form'] = CassetteImageForm()
            # context['cassette_image_addons_form'] = CassetteImageAddonsForm()
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
        for view in Image.View:
            print(view)
        # image_instance, _ = Image.objects.get_or_create(cassette=self.object)
        price_instance, _ = CassettePrice.objects.get_or_create(cassette=self.object)
        context = super(CassetteUpdateView, self).get_context_data(**kwargs)
        # Translators: Catalog view title for page ('Редактировать предмет')
        context['page_title'] = gettext('Edit Item')
        if self.request.POST:
            # context['imageformset'] = ImageFormSet(self.request.POST,
            #                                        instance=self.object.images.all())
            # context['cassette_image_form'] = CassetteImageForm(self.request.POST, self.request.FILES, instance=image_instance)
            # context['cassette_image_addons_form'] = CassetteImageAddonsForm(self.request.POST, self.request.FILES, instance=image_instance)
            context['cassette_price_form'] = CassettePriceForm(self.request.POST, instance=price_instance)

        else:
            context['imageformset'] = ImageFormSet(instance=self.object)
            # context['cassette_image_form'] = CassetteImageForm(instance=image_instance)
            # context['cassette_image_addons_form'] = CassetteImageAddonsForm(instance=image_instance)
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
