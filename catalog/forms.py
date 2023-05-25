from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Fieldset, HTML, Div, Field
from django import forms
from catalog.models import Cassette, CassettesImage, CassetteBarcode, CassetteFrequencyResponse, CassettePrice, \
    CASSETTECONDITION
from django.forms.models import BaseInlineFormSet, inlineformset_factory


class CassetteCreateForm(forms.ModelForm):
    """Основная форма на странице апдейта кассеты"""
    class Meta:
        model = Cassette
        fields = '__all__'
        exclude = ['user']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['price'] = forms.ModelChoiceField(queryset=CassettePrice.objects.filter(cassette=self.instance))
        self.fields['condition'] = forms.ChoiceField(choices=CASSETTECONDITION)
        self.helper = FormHelper(self)
        self.helper.label_class = 'table__inputs-text settings__text-bold'
        self.helper.field_class = 'table__inputs-value'
        self.helper.layout = Layout(
            Div(
                Div(
                    'brand',
                    'manufacturer',
                    'model',
                    'series',
                    'tape_length',
                    'type',
                    'year_release',
                    css_class='table__inputs',
                ),
                Div(
                    HTML("""<p class="settings__title-block">Комментарий</p>"""),
                    'comment',
                    css_class='settings__textarea'
                ),
                Div(
                    Div(
                        HTML("""<p class="settings__title-block">Дополнительные параметры</p>"""),
                        Div(
                            'slim_case',
                            'coil',
                            css_class='checkbox-cust settings__checkbox',

                        ),

                    ),
                    css_class='settings__wrapper-checkbox_objects',
                ),
            ),
        )

        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'input-cust'


class CassetteImageForm(forms.ModelForm):
    """Форма добавления изображений"""
    class Meta:
        model = CassettesImage
        fields = '__all__'
        exclude = ('cassette',)


class CassetteBarcodeForm(forms.ModelForm):
    """Форма добавления штрихкода"""
    class Meta:
        model = CassetteBarcode
        fields = '__all__'
        exclude = ('cassette',)


class CassetteFrequencyResponseForm(forms.ModelForm):
    """Форма добавления частотной характеристики кассеты"""
    class Meta:
        model = CassetteFrequencyResponse
        fields = '__all__'
        exclude = ('cassette',)


class CassettePriceForm(forms.ModelForm):
    """Форма добавления цены"""
    class Meta:
        model = CassettePrice
        fields = ['price', 'condition']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper(self)
        self.helper.label_class = 'table__inputs-text settings__text-bold'
        self.helper.field_class = 'table__inputs-value'
        self.helper.layout = Layout(
            Div(
                Div(
                    Div(
                        'price',
                        'condition',
                    ),
                ),
                css_class='settings__wrapper-checkbox_objects',
            ),
        )

        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'input-cust'


CassetteImageFormSet = inlineformset_factory(
    Cassette, CassettesImage, form=CassetteImageForm,
    extra=12, can_delete=True, can_delete_extra=True
)
CassetteBarcodeFormSet = inlineformset_factory(
    Cassette, CassetteBarcode, form=CassetteBarcodeForm,
    extra=1, can_delete=True, can_delete_extra=True
)
CassetteFrequencyResponseFormSet = inlineformset_factory(
    Cassette, CassetteFrequencyResponse, form=CassetteFrequencyResponseForm,
    extra=1, can_delete=True, can_delete_extra=True
)

CassettePriceFormSet = inlineformset_factory(
    Cassette, CassettePrice, form=CassettePriceForm,
    extra=1, can_delete=True, can_delete_extra=True
)
