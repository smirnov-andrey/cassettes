from django import forms
from django.core import validators
from django.utils.translation import gettext as _


from catalog.models import (Cassette, CassettesImage, CassettePrice,
                            CassetteComment)


class CassetteCreateForm(forms.ModelForm):
    """Основная форма на странице апдейта кассеты"""
    class Meta:
        model = Cassette
        fields = [
            'brand',
            'manufacturer',
            'model',
            'series',
            'tape_length',
            'type',
            'year_release',
            'coil',
            'slim_case',
            'comment'
        ]
        labels = {
            'brand': _('Brand'),
            'manufacturer': _('Manufacturer'),
            'model': _('Model'),
            'series': _('Series'),
            'tape_length': _('Tape length'),
            'type': _('Type'),
            'year_release': _('Brand'),
            'coil': _('Coil'),
            'slim_case': _('Slim case'),
            'comment': _('Comment'),
        }
        widgets = {
            'brand': forms.Select(attrs={'class': 'input-cust'}),
            'manufacturer': forms.Select(attrs={'class': 'input-cust'}),
            'model': forms.Select(attrs={'class': 'input-cust'}),
            'series': forms.Select(attrs={'class': 'input-cust'}),
            'tape_length': forms.Select(attrs={'class': 'input-cust'}),
            'type': forms.Select(attrs={'class': 'input-cust'}),
            'year_release': forms. NumberInput(attrs={'class': 'input-cust'}),
            'coil': forms.CheckboxInput(attrs={
                'class': 'checkbox-cust__input',
                'name': 'parametrs',
                'id': 'parametrs-1'
            }),
            'slim_case': forms.CheckboxInput(attrs={
                'class': 'checkbox-cust__input',
                'name': 'parametrs',
                'id': 'parametrs-2'
            }),
            'comment': forms.Textarea(attrs={
                'class': 'textarea-cust',
                'placeholder': _('Comment'),
                'rows': '5',
            }),
        }


class CassetteImageForm(forms.ModelForm):
    """Форма добавления изображений"""
    class Meta:
        model = CassettesImage
        fields = [
            'package_front_side',
            'package_back_side',
            'package_end_side',
            'box_front_side',
            'box_back_side',
            'description_one',
            'description_two',
            'item_side_a',
            'item_side_b',
            'box_general_view',
            'item_general_view',
            'general_view',
        ]
        labels = {
            'package_front_side': _('Front side of the package'),
            'package_back_side': _('Back side of the package'),
            'package_end_side': _('End side'),
            'box_front_side': _('Front side of the box'),
            'box_back_side': _('Back side of the box'),
            'description_one': _('Description 1'),
            'description_two': _('Description 2'),
            'item_side_a': _('Item (Side A)'),
            'item_side_b': _('Item (Side B)'),
            'box_general_view': _('General view (Box)'),
            'item_general_view': _('General view (Item)'),
            'general_view': _('General view'),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'invisible add-photo__inputChange'


class CassetteImageAddonsForm(forms.ModelForm):
    """Форма добавления изображений"""
    class Meta:
        model = CassettesImage
        fields = [
            'frequency_response',
            'barcode'
        ]
        labels = {
            'frequency_response': _('Frequency Response'),
            'barcode': _('Barcode'), #'Добавить штрихкод'
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'fileInput invisible'


class CassettePriceForm(forms.ModelForm):
    """Форма добавления цены"""

    class Meta:
        model = CassettePrice
        fields = [
            'poor',
            'good',
            'very_good',
            'excellent',
            'near_mint',
            'mint',
        ]
        labels = {
            'poor': _('Poor'),
            'good': _('Good'),
            'very_good': _('Very good'),
            'excellent': _('Excellent'),
            'near_mint': _('Near mint'),
            'mint': _('Mint'),
        }
        validators = {
            'poor': [validators.MinValueValidator(limit_value=1)],
            'good': [validators.MinValueValidator(limit_value=1)],
            'very_good': [validators.MinValueValidator(limit_value=1)],
            'excellent': [validators.MinValueValidator(limit_value=1)],
            'near_mint': [validators.MinValueValidator(limit_value=1)],
            'mint': [validators.MinValueValidator(limit_value=1)]
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'input-cust input-cust_fz14'


class CassetteCommentForm(forms.ModelForm):
    """Форма добавления коммментария"""

    class Meta:
        model = CassetteComment
        fields = ['user', 'cassette','comment', ]
        labels = {'comment': '', }
        validators = {'comment': [validators.MinLengthValidator(limit_value=1, message=_('Please leave a comment'))], } #'Оставьте комментарий'
        widgets = {
            'user': forms.HiddenInput(),
            'cassette': forms.HiddenInput(),
            'comment': forms.Textarea(attrs={'class': 'textarea-cust', 'name': 'comments-add', 'id': 'comments-add', 'placeholder': _('Leave a comment'), 'rows': '5'}),
        }
