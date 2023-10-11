from django.db.models import F, Count
from django.shortcuts import render

from catalog.models import Category, Cassette, CassetteComment
from users.models import User


def homepage(request):
    queryset = Category.objects.annotate(
        cassette_count=Count('cassettes'),
    ).filter(
        is_published=True,
        is_published_to_home=True
    )
    context = {
        'collector_list': User.objects.order_by(F('rating').desc(nulls_last=True))[:5],
        'cassette_list': Cassette.objects.select_related(
            'category', 'brand', 'tape_type', 'model', 'technology',
            'manufacturer', 'series', 'sort', 'tape_length', 'country'
        ).prefetch_related(
            'images'
        ).order_by(
            '-updated',
        ).all()[:7],
        'category_audio': queryset.filter(type=Category.AUDIO),
        'category_video': queryset.filter(type=Category.VIDEO),
        'comment_list': CassetteComment.objects.filter(is_published=True)[:10],
    }
    return render(request, 'core/index.html', context)
