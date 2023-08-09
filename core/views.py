from django.db.models import F
from django.shortcuts import render

from catalog.models import CassetteCategory, Cassette, CassetteComment
from users.models import User


def homepage(request):
    queryset = CassetteCategory.objects.filter(is_published=True, is_published_to_home=True)

    context = {
        'collector_list': User.objects.order_by(F('rating').desc(nulls_last=True))[:5],
        'cassette_list': Cassette.objects.all()[:7],
        'category_audio': queryset.filter(type=CassetteCategory.AUDIO),
        'category_video': queryset.filter(type=CassetteCategory.VIDEO),
        'comment_list': CassetteComment.objects.filter(is_published=True)[:10],
    }
    return render(request, 'core/index.html', context)
