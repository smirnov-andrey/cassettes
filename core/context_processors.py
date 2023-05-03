from catalog.models import CassetteCategory


def categories(request):
    return {'category_list': CassetteCategory.objects.all()}
