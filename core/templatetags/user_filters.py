from django import template

from catalog.models import Cassette

# В template.Library зарегистрированы все встроенные теги и фильтры шаблонов;
# добавляем к ним и наш фильтр.
register = template.Library()


@register.filter
def addclass(field, css):
    return field.as_widget(attrs={'class': css})


@register.filter
def image_cover(queryset):
    if queryset.exists():
        if queryset.filter(is_cover=True).exists():
            return queryset.filter(is_cover=True).first()
        else:
            return queryset.order_by('view').first()
    return None


@register.simple_tag
def cassettes_count(category, brand):
    return Cassette.objects.filter(category_id=category, brand=brand).count()


# синтаксис @register... , под который описана функция addclass() -
# это применение "декораторов", функций, меняющих поведение функций
# Не бойтесь соб@к