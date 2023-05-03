from django.shortcuts import render
from django.views.generic import DetailView, ListView

from catalog.models import CassetteCategory, Cassette
from users.models import User


def homepage(request):
    context = {
        'collector_list':User.objects.all()[:5],
        'cassette_list': Cassette.objects.all()[:7] ,
        'category_list': CassetteCategory.objects.all(),
    }
    return render(request, 'core/index.html', context)


