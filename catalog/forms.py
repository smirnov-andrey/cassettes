from django import forms
from django.core import validators

from catalog.models import Cassette, CassettesImage, CassettePrice
from django.forms.models import inlineformset_factory


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
            'brand': 'Бренд',
            'manufacturer': 'Производитель',
            'model': 'Модель',
            'series': 'Серия',
            'tape_length': 'Длина ленты',
            'type': 'Тип кассеты',
            'year_release': 'Год выпуска',
            'coil': 'Катушка',
            'slim_case': 'Слим кейс',
            'comment': 'Комментарий',
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
                'placeholder': 'Комментарий',
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
            'package_front_side': 'Передняя сторона упаковки',
            'package_back_side': 'Задняя сторона упаковки',
            'package_end_side': 'Торец упаковки',
            'box_front_side': 'Передняя сторона коробки',
            'box_back_side': 'Задняя сторона коробки',
            'description_one': 'Описание 1',
            'description_two': 'Описание 2',
            'item_side_a': 'Предмет (Сторона А)',
            'item_side_b': 'Предмет (Сторона Б)',
            'box_general_view': 'Общий вид (Коробка)',
            'item_general_view': 'Общий вид (Предмет)',
            'general_view': 'Общий вид',
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
            'frequency_response': 'Frequency Response',
            'barcode': 'Добавить штрихкод'
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'fileInput invisible'


class CassettePriceForm(forms.ModelForm):
    """Форма добавления цены"""
    price = forms.IntegerField(label='Цена',
                               validators=[validators.MinValueValidator(limit_value=1)],
                               widget=forms.NumberInput(attrs={'class': 'input-cust'}),
                               )

    class Meta:
        model = CassettePrice
        fields = ['condition', 'price']
        widgets = {
            'condition': forms.Select(attrs={'class': 'input-cust'}),
            'price': forms.NumberInput(attrs={'class': 'input-cust'})
        }
        validators = {
            'price': [validators.MinValueValidator(limit_value=1)]
        }


CassettePriceFormSet = inlineformset_factory(
    Cassette, CassettePrice, form=CassettePriceForm,
    extra=1, can_delete=True, can_delete_extra=True
)
